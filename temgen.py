import errno
import glob
import json
import os
import re
import sys
import tempfile
import tomllib
import semver
import xml.etree.ElementTree as XMLTree
from xml.etree.ElementTree import Element as XMLElement
from pathlib import Path

from constants import regex, names
from statement.abstract_statement import AbstractStatement
from ui.abstract_ui_manager import AbstractUiManager
from ui.basic.make_basic_ui_from_name import make_basic_ui_from_name
from ui.basic.tkinter_basic_ui import TkinterBasicUi
from util import random_string
from util.application_directories import ApplicationDirectories
from ui.basic.abstract_basic_ui import AbstractBasicUi
from util.log import make_logger_from_config
from variables.variables_dict import VariablesDict


class Temgen:
    VERSION = semver.Version.parse('0.9.0-dev')
    APPLICATION_DIRECTORIES = ApplicationDirectories(names.LOWER_PROGRAM_NAME)

    def __init__(self, basic_ui: AbstractBasicUi | None, ui_manager: AbstractUiManager | None = None, **kargs):
        self.__load_config(kargs)
        logger = kargs.get("logger")
        if logger is None:
            logger = make_logger_from_config(self.__config.get("logging"), True,
                                             app_dirs=self.APPLICATION_DIRECTORIES)[0]
        self.__logger = logger
        self.__define_signal_handler()
        if basic_ui is None:
            basic_ui_name = self.__config.get("ui", dict()).get("basic", TkinterBasicUi.NAME)
            basic_ui = make_basic_ui_from_name(basic_ui_name)
        self.__basic_ui = basic_ui
        self.__ui_manager = ui_manager
        if self.__ui_manager is not None:
            self.__ui_manager.set_temgen(self)
        self.__variables = VariablesDict(self.__logger)
        self.__init_variables(kargs)
        settings = self.__config["settings"]
        self.__templates_dirpaths = self.APPLICATION_DIRECTORIES.data_dirpaths("templates")
        template_dirpaths = settings.get("templates_dirs", [])
        assert isinstance(template_dirpaths, list)
        self.__templates_dirpaths.extend([Path(template_dirpath) for template_dirpath in template_dirpaths])
        self.__templates_dirpaths.append(Path("."))
        self.__check_template_activated = bool(kargs.get("check_template", settings.get("check_template", False)))

    def __load_config(self, kargs):
        default_config_path = self.APPLICATION_DIRECTORIES.settings_dirpath() / "config/default.toml"
        config_path = Path(kargs.get("config_path", default_config_path))
        if config_path.exists():
            with open(config_path, 'rb') as config_file:
                self.__config = tomllib.load(config_file)
        else:
            self.__config = dict()
        self.__config.setdefault("settings", dict())

    def __define_signal_handler(self):
        def signal_handler(sig, frame):
            self.logger.warning(f"Abort requested!")
            sys.exit("Abort temgen.")

        import signal
        signal.signal(signal.SIGINT, signal_handler)

    def __init_variables(self, kargs):
        config_variables = self.__config.setdefault("variables", dict())
        self.__variables.update_vars_from_dict(config_variables)
        var_files = kargs.get("var_files", [])
        self.__variables.update_vars_from_files(var_files)
        var_dict = kargs.get("var_dict", [])
        self.__variables.update_vars_from_dict(var_dict)
        self.__config.setdefault("ui", dict()).setdefault("extra", dict())

    @property
    def logger(self):
        return self.__logger

    def config(self):
        return self.__config

    def basic_ui(self):
        return self.__basic_ui

    def ui_cmd(self, ui: str):
        return self.__config["ui"]["extra"].get(ui, ui)

    def init_variables(self):
        return self.__variables

    def templates_dirpaths(self):
        return self.__templates_dirpaths

    def check_template_activated(self):
        return self.__check_template_activated

    def call_ui(self, ui: str, statement: AbstractStatement):
        if len(ui.strip()) == 0:
            parent_statement = statement.parent_statement()
            return VariablesDict(self.logger) if parent_statement is not None else statement.variables()
        if self.__ui_manager:
            parent_statement = statement.parent_statement()
            if parent_statement is not None:
                variables = VariablesDict(self.logger)
            else:
                variables = statement.variables()
            from variables.variables_map import VariablesMap
            ui_treated = self.__ui_manager.call_ui(ui, variables, VariablesMap(statement, False))
            if ui_treated:
                return variables
        with tempfile.NamedTemporaryFile("w", delete=False) as vars_file:
            input_var_filepath = Path(vars_file.name)
            app_dirpath = Temgen.APPLICATION_DIRECTORIES.tmp_dirpath()
            output_var_filepath = app_dirpath / f"{random_string.random_lower_sisy_string(8)}.json"
            cmd = self.ui_cmd(ui)
            formatted_cmd: str = cmd.format(input_var_filepath, output_var_filepath,
                                            input_file=input_var_filepath, output_file=output_var_filepath,
                                            python=sys.executable)
            if formatted_cmd.find(str(input_var_filepath)) != -1:
                parent_statement = statement.parent_statement()
                if parent_statement is not None:
                    variables = parent_statement.get_variables_from_root()
                else:
                    variables = statement.variables().clone()
            else:
                variables = VariablesDict(self.logger)
            json.dump(variables, vars_file)
        cmd_res = os.system(formatted_cmd)
        if cmd_res != 0:
            raise RuntimeError(f"Execution of ui did not work well (returned {cmd_res}). "
                               f"command: {formatted_cmd}")
        variables.update_vars_from_files([output_var_filepath])
        input_var_filepath.unlink(missing_ok=True)
        output_var_filepath.unlink(missing_ok=True)
        return variables

    def find_template_file(self, template_path: Path, version_attr) -> Path:
        template_dpath = template_path.parent
        template_fname = template_path.name
        has_xml_suffix = template_path.suffix == ".xml"
        rmatch = re.fullmatch(regex.TEMPLATE_FILENAME_REGEX, template_fname)
        if not rmatch:
            if not has_xml_suffix:
                raise RuntimeError(f"The path '{template_path}' is not a valid path.")
            elif template_path.exists():
                return template_path
            else:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(template_path))
        if has_xml_suffix:
            if version_attr:
                print("WARNING: The attribute version is ignored as the provided template is a file path "
                      f"(version or extension is contained in the path): '{template_path}'.")
            for template_root_dpath in self.__templates_dirpaths:
                xml_path = template_root_dpath / template_path
                if xml_path.exists():
                    return xml_path
            raise FileNotFoundError(errno.ENOENT, "Template not found", str(template_path))
        template_name = rmatch.group(regex.TEMPLATE_FILENAME_REGEX_NAME_GROUP_ID)
        template_version = rmatch.group(regex.TEMPLATE_FILENAME_REGEX_VERSION_GROUP_ID)
        if template_version:
            raise RuntimeError(f"The extension '.xml' is missing at the end of the template path: '{template_path}'.")
        if not version_attr:
            for template_root_dpath in self.__templates_dirpaths:
                xml_path = template_root_dpath / f"{template_path}.xml"
                if xml_path.exists():
                    return xml_path
            name_pattern = f"{template_name}-*.*.*.xml"
            expected_major = 0
            expected_minor = 0
            expected_patch = 0
        else:
            rmatch = re.fullmatch(regex.TRI_VERSION_REGEX, version_attr)
            if not rmatch:
                raise RuntimeError(f"Template version is not a valid version: '{version_attr}'.")
            expected_major = int(rmatch.group(regex.TRI_VERSION_REGEX_MAJOR_GROUP_ID))
            name_pattern = f"{template_name}-{expected_major}"
            expected_minor = rmatch.group(regex.TRI_VERSION_REGEX_MINOR_GROUP_ID)
            if expected_minor:
                name_pattern = f"{name_pattern}.{expected_minor}"
                expected_minor = int(expected_minor)
            else:
                name_pattern = f"{name_pattern}.*"
                expected_minor = 0
            expected_patch = rmatch.group(regex.TRI_VERSION_REGEX_PATCH_GROUP_ID)
            if expected_patch:
                name_pattern = f"{name_pattern}.{expected_patch}"
                expected_patch = int(expected_patch)
            else:
                name_pattern = f"{name_pattern}.*"
                expected_patch = 0
            name_pattern = f"{name_pattern}.xml"
        template_fpath = None
        for template_root_dpath in self.__templates_dirpaths:
            t_dir = template_root_dpath / template_dpath
            template_file_list = glob.glob(name_pattern, root_dir=t_dir)
            template_file_list.sort(reverse=True)
            template_fpath = None
            for template_file in template_file_list:
                rmatch = re.fullmatch(regex.TEMPLATE_FILENAME_REGEX, Path(template_file).name)
                if rmatch:
                    if not version_attr:
                        template_fpath = f"{t_dir}/{template_file}"
                        break
                    template_file_minor = int(rmatch.group(regex.TEMPLATE_FILENAME_REGEX_MINOR_GROUP_ID))
                    template_file_patch = int(rmatch.group(regex.TEMPLATE_FILENAME_REGEX_PATCH_GROUP_ID))
                    if template_file_minor > expected_minor \
                            or template_file_minor == expected_minor and template_file_patch >= expected_patch:
                        template_fpath = f"{t_dir}/{template_file}"
                        break
            if template_fpath is not None:
                break
        if template_fpath is None:
            raise RuntimeError(f"No template '{template_fname}' compatible with version {version_attr} found "
                               f"in {template_dpath}.")
        return Path(template_fpath)

    def treat_template_file(self, template_filepath: Path, output_dir=None, ui=None):
        from statement.template_statement import TemplateStatement
        with open(template_filepath, 'r') as template_file:
            element_tree = XMLTree.parse(template_file)
        output_dir = self.__resolve_output_dir(output_dir)
        template_statement = TemplateStatement(element_tree.getroot(), None,
                                               temgen=self,
                                               template_filepath=template_filepath,
                                               variables=self.init_variables().clone(),
                                               output_dirpath=Path(output_dir),
                                               ui=ui)
        template_statement.run()

    def find_and_treat_template_file(self, template_path: Path, version: str | None = None, output_dir=None, ui=None):
        template_filepath = self.find_template_file(template_path, version)
        self.treat_template_file(template_filepath, output_dir, ui)

    def treat_template_xml_string(self, template_str: str, output_dir=None, ui=None):
        from statement.template_statement import TemplateStatement
        root_element = XMLTree.fromstring(template_str)
        output_dir = self.__resolve_output_dir(output_dir)
        template_statement = TemplateStatement(root_element, None,
                                               temgen=self,
                                               variables=self.init_variables().clone(),
                                               output_dirpath=Path(output_dir),
                                               ui=ui)
        template_statement.run()

    @staticmethod
    def check_template(root_element: XMLElement):
        valid_statement_names = ["dir", "file", "contents",
                                 "if", "then", "else", "match", "case", "block",
                                 "vars", "var",
                                 "exec", "random",
                                 "template"]
        attr_regex = re.compile(r"[a-z]+(-[a-z]+)*")
        Temgen.__check_template_xml_element(root_element, valid_statement_names, attr_regex)

    @staticmethod
    def __check_template_xml_element(element: XMLElement, valid_statement_names: list[str], attr_regex: re.Pattern):
        if element.tag not in valid_statement_names:
            raise RuntimeError(f"Unexpected statement in template: '{element.tag}'.")
        for attr in element.attrib.keys():
            if not re.fullmatch(attr_regex, attr):
                raise RuntimeError(f"Bad attribute name in {element.tag} statement: '{attr}'.")
        for child in element:
            Temgen.__check_template_xml_element(child, valid_statement_names, attr_regex)

    @staticmethod
    def __resolve_output_dir(output_dir):
        if output_dir is None:
            output_dir = Path.cwd()
        if not output_dir.exists():
            raise FileNotFoundError(f"The provided output directory does not exist: '{output_dir}'.")
        return output_dir
