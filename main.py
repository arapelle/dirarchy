import argparse
import glob
import json
import os
import platform
import random
import tempfile
import xml.etree.ElementTree as XMLTree
from enum import StrEnum, auto
from pathlib import Path
import re
import io

import constants
import random_string
from tkinter_ask_dialog import TkinterAskDialog
from terminal_ask_dialog import TerminalAskDialog
import version
from variables_dict import VariablesDict


class RegexFullMatch:
    def __init__(self, regex):
        if isinstance(regex, re.Pattern):
            self.__regex = regex
        else:
            self.__regex = re.compile(regex)

    def __call__(self, value_to_check: str):
        return re.fullmatch(self.__regex, value_to_check)


class Dirarchy:
    class UiType(StrEnum):
        TKINTER = auto()
        TERMINAL = auto()

    # classic_name (like hello_world_01)
    CLASSIC_NAME_RESTR = r'[a-zA-Z][a-zA-Z0-9]*(_[a-zA-Z0-9]+)*'

    # tri_version (like 0.1.0)
    TRI_VERSION_RESTR = r'(0|[1-9]\d*)(\.(0|[1-9]\d*))?(\.(0|[1-9]\d*))?'
    TRI_VERSION_REGEX = re.compile(TRI_VERSION_RESTR)
    TRI_VERSION_REGEX_MAJOR_GROUP_ID = 1
    TRI_VERSION_REGEX_MINOR_GROUP_ID = 3
    TRI_VERSION_REGEX_PATCH_GROUP_ID = 5

    # full_tri_version (like 0.1.0, or 0.1 or 0)
    FULL_TRI_VERSION_RESTR = r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)'
    FULL_TRI_VERSION_REGEX = re.compile(FULL_TRI_VERSION_RESTR)
    FULL_TRI_VERSION_REGEX_MAJOR_GROUP_ID = 1
    FULL_TRI_VERSION_REGEX_MINOR_GROUP_ID = 2
    FULL_TRI_VERSION_REGEX_PATCH_GROUP_ID = 3

    # template_filename := (classic_name)-(tri_version)\.xml
    TEMPLATE_FILENAME_RESTR = f"({CLASSIC_NAME_RESTR})(-({FULL_TRI_VERSION_RESTR}))?(\.xml)?"
    TEMPLATE_FILENAME_REGEX = re.compile(f"({CLASSIC_NAME_RESTR})(-({FULL_TRI_VERSION_RESTR}))?(\.xml)?")
    TEMPLATE_FILENAME_REGEX_NAME_GROUP_ID = 1
    TEMPLATE_FILENAME_REGEX_VERSION_GROUP_ID = 3
    TEMPLATE_FILENAME_REGEX_MAJOR_GROUP_ID = 5
    TEMPLATE_FILENAME_REGEX_MINOR_GROUP_ID = 6
    TEMPLATE_FILENAME_REGEX_PATCH_GROUP_ID = 7
    TEMPLATE_FILENAME_REGEX_EXT_GROUP_ID = 8
    # namespace_path := namespace_name(/+namespace_name)*/*
    NAMESPACE_NAME_RESTR = CLASSIC_NAME_RESTR
    NAMESPACE_PATH_RESTR = fr"({NAMESPACE_NAME_RESTR})(/+{NAMESPACE_NAME_RESTR})*/*"
    # template_path := (namespace_path/)?template_name
    TEMPLATE_PATH_REGEX = re.compile(f"({NAMESPACE_PATH_RESTR}/)?({TEMPLATE_FILENAME_RESTR})")
    TEMPLATE_PATH_REGEX_DIR_GROUP_ID = 1
    TEMPLATE_PATH_REGEX_FILENAME_GROUP_ID = 6
    TEMPLATE_PATH_REGEX_NAME_GROUP_ID = 7
    TEMPLATE_PATH_REGEX_VERSION_GROUP_ID = 10
    TEMPLATE_PATH_REGEX_MAJOR_GROUP_ID = 11
    TEMPLATE_PATH_REGEX_MINOR_GROUP_ID = 12
    TEMPLATE_PATH_REGEX_PATCH_GROUP_ID = 13

    VAR_NAME_REGEX = re.compile(r'\A[a-zA-Z][a-zA-Z0-9_]*\Z')
    VAR_REGEX = re.compile(r"\{([a-zA-Z][a-zA-Z0-9_]*)\}|(\{\{|\}\})")
    VAR_NAME_GROUP_ID = 1
    SKIP_GROUP_ID = VAR_NAME_GROUP_ID + 1

    def __init__(self, argv=None):
        self.__source_file_stack = []
        self.__template_root_dpaths = self.__global_template_roots()
        self.__template_root_dpaths.append(Path("."))
        self.__variables = VariablesDict()
        self._args = self._parse_args(argv)
        match self._args.ui:
            case Dirarchy.UiType.TERMINAL:
                self.__ui = TerminalAskDialog()
            case Dirarchy.UiType.TKINTER:
                self.__ui = TkinterAskDialog()
            case _:
                raise Exception(f"Unknown I/O: '{self._args.io}'")
        self.__set_variables_from_args()

    def run(self):
        if Path(self._args.output_dir).exists():
            self.treat_xml_file(self._args.dirarchy_xml_file, self._args.output_dir)
        else:
            raise Exception(f"The provided output directory does not exist: '{self._args.output_dir}'.")

    def __set_variables_from_args(self):
        if self._args.var:
            for key, value in self._args.var:
                self.__variables[key] = value
                print(f"Set variable {key}={value}")
        if self._args.var_file:
            for var_file in self._args.var_file:
                with open(var_file) as vars_file:
                    var_dict = json.load(vars_file)
                    if not isinstance(var_dict, dict):
                        raise Exception(f"The variables file '{var_file}' does not contain a valid JSON dict.")
                    for key, value in var_dict.items():
                        self.__variables[key] = value
                        print(f"Set variable {key}={value}")
        if self._args.custom_ui:
            self.__set_variables_from_custom_ui(self._args.custom_ui)

    def __set_variables_from_custom_ui(self, cmd: str):
        with tempfile.NamedTemporaryFile("w", delete=False) as vars_file:
            var_file_fpath = Path(vars_file.name)
            json.dump(self.__variables, vars_file)
        cmd_with_args = f"{cmd} {var_file_fpath}"
        cmd_res = os.system(cmd_with_args)
        if cmd_res != 0:
            raise RuntimeError(f"Execution of custom ui did not work well (returned {cmd_res}). "
                               f"command: {cmd_with_args}")
        with open(var_file_fpath) as vars_file:
            self.__variables = VariablesDict(json.load(vars_file))
        var_file_fpath.unlink(missing_ok=True)

    def _parse_args(self, argv=None):
        prog_name = 'dirarchy'
        prog_desc = 'A tool generating a directory architecture based on a template.'
        argparser = argparse.ArgumentParser(prog=prog_name, description=prog_desc)
        argparser.add_argument('--version', action='version', version=f'{prog_name} {version.VERSION}')
        argparser.add_argument('-K', f'--{Dirarchy.UiType.TKINTER}'.lower(), action='store_const',
                               dest='ui', const=Dirarchy.UiType.TKINTER, help='Use tkinter I/O.')
        argparser.add_argument('-T', f'--{Dirarchy.UiType.TERMINAL}'.lower(), action='store_const',
                               dest='ui', const=Dirarchy.UiType.TERMINAL, default='terminal', help='Use terminal I/O.')
        argparser.add_argument('-C', '--custom-ui', metavar='custom_ui_cmd',
                               help='Use a custom user interface to set variables before treating them with dirarchy. '
                                    '(Executing custom_ui_cmd in shell is expected to use the desired custom '
                                    'interface.)')
        argparser.add_argument('-o', '--output-dir', metavar='dir_path',
                               default=Path.cwd(),
                               help='The directory where to generate the desired hierarchy (dir or file).')
        argparser.add_argument('-v', '--var', metavar='key=value', nargs='+',
                               type=Dirarchy.var_from_key_value_str,
                               help='Set variables.')
        argparser.add_argument('--var-file', metavar='var_json_files', nargs='+',
                               help='Set variables from a JSON files.')
        argparser.add_argument('dirarchy_xml_file',
                               help='The dirarchy XML file to process.')
        args = argparser.parse_args(argv)
        if args.ui is None:
            args.ui = Dirarchy.UiType.TKINTER
        return args

    @classmethod
    def var_from_key_value_str(cls, key_value_str: str):
        key, value = key_value_str.split('=')
        if re.match(Dirarchy.VAR_NAME_REGEX, key):
            return key, value
        raise RuntimeError(key_value_str)

    def __treat_action_node(self, node: XMLTree.Element, working_dir):
        assert node is not None
        match node.tag:
            case "dir":
                return self.__treat_dir_node(node, working_dir)
            case "file":
                return self.__treat_file_node(node, working_dir)
            case "if":
                return self.__treat_if_node(node, working_dir)
            case "match":
                return self.__treat_match_node(node, working_dir)
            case _:
                raise Exception(f"Unknown node type: {node.tag}.")

    def __treat_dir_node(self, dir_node: XMLTree.Element, working_dir: Path):
        template_fpath = dir_node.attrib.get('template', None)
        if template_fpath is not None:
            print(f"<dir  {template_fpath}>")
            template_fpath = self.__find_template(dir_node, template_fpath)
            working_dir = self.__treat_xml_file(template_fpath, working_dir, "dir")
        else:
            dir_path = self.__fsys_node_path(dir_node)
            print(f"<dir  {working_dir}/ {dir_path}>")
            assert 'template' not in dir_node.attrib
            working_dir /= dir_path
            working_dir.mkdir(parents=True, exist_ok=True)
        self.__treat_action_children_nodes_of(dir_node, working_dir)
        return working_dir

    def __find_template(self, node, template_fpath):
        assert 'path' not in node.attrib
        template_fpath = Path(self.__format_str(template_fpath))
        template_dpath = template_fpath.parent
        template_fname = template_fpath.name
        rmatch = re.fullmatch(self.TEMPLATE_FILENAME_REGEX, template_fname)
        if not rmatch:
            raise RuntimeError(f"The path '{template_fpath}' is not a valid path.")
        version_attr = node.attrib.get('template-version', None)
        if version_attr:
            version_attr = self.__format_str(version_attr)
        template_name = rmatch.group(self.TEMPLATE_FILENAME_REGEX_NAME_GROUP_ID)
        template_ext = rmatch.group(self.TEMPLATE_FILENAME_REGEX_EXT_GROUP_ID)
        if template_ext is not None:
            if version_attr:
                print("WARNING: The attribute version is ignored as the provided template is a file path "
                      f"(version or extension is contained in the path): '{template_fpath}'.")
            for template_root_dpath in self.__template_root_dpaths:
                xml_path = template_root_dpath / template_fpath
                if xml_path.exists():
                    return xml_path
            raise RuntimeError(f"Template not found: '{template_fpath}'.")
        template_version = rmatch.group(self.TEMPLATE_FILENAME_REGEX_VERSION_GROUP_ID)
        if template_version:
            raise RuntimeError(f"The extension '.xml' is missing at the end of the template path: '{template_fpath}'.")
        if not version_attr:
            for template_root_dpath in self.__template_root_dpaths:
                xml_path = template_root_dpath / f"{template_fpath}.xml"
                if xml_path.exists():
                    return xml_path
            name_pattern = f"{template_name}-*.*.*.xml"
            expected_major = 0
            expected_minor = 0
            expected_patch = 0
        else:
            rmatch = re.fullmatch(self.TRI_VERSION_REGEX, version_attr)
            if not rmatch:
                raise RuntimeError(f"Template version is not a valid version: '{version_attr}'.")
            expected_major = int(rmatch.group(self.TRI_VERSION_REGEX_MAJOR_GROUP_ID))
            name_pattern = f"{template_name}-{expected_major}"
            expected_minor = rmatch.group(self.TRI_VERSION_REGEX_MINOR_GROUP_ID)
            if expected_minor:
                name_pattern = f"{name_pattern}.{expected_minor}"
                expected_minor = int(expected_minor)
            else:
                name_pattern = f"{name_pattern}.*"
                expected_minor = 0
            expected_patch = rmatch.group(self.TRI_VERSION_REGEX_PATCH_GROUP_ID)
            if expected_patch:
                name_pattern = f"{name_pattern}.{expected_patch}"
                expected_patch = int(expected_patch)
            else:
                name_pattern = f"{name_pattern}.*"
                expected_patch = 0
            name_pattern = f"{name_pattern}.xml"
        for template_root_dpath in self.__template_root_dpaths:
            t_dir = template_root_dpath / template_dpath
            template_file_list = glob.glob(name_pattern, root_dir=t_dir)
            template_file_list.sort(reverse=True)
            template_fpath = None
            for template_file in template_file_list:
                rmatch = re.fullmatch(self.TEMPLATE_FILENAME_REGEX, Path(template_file).name)
                if rmatch:
                    if not version_attr:
                        template_fpath = f"{t_dir}/{template_file}"
                        break
                    template_file_minor = int(rmatch.group(self.TEMPLATE_FILENAME_REGEX_MINOR_GROUP_ID))
                    template_file_patch = int(rmatch.group(self.TEMPLATE_FILENAME_REGEX_PATCH_GROUP_ID))
                    if template_file_minor > expected_minor \
                            or template_file_minor == expected_minor and template_file_patch >= expected_patch:
                        template_fpath = f"{t_dir}/{template_file}"
                        break
            if template_fpath is not None:
                break
        if template_fpath is None:
            raise RuntimeError(f"No template '{template_fname}' compatible with version {version_attr} found "
                               f"in {template_dpath}.")
        return template_fpath

    @staticmethod
    def __global_template_roots():
        roots = []
        roots.extend(Dirarchy.system_template_roots())
        roots.extend(Dirarchy.environment_template_roots())
        return roots

    @staticmethod
    def environment_template_roots():
        roots = []
        dirarchy_templates_path = os.environ.get(f'{constants.UPPER_PROGRAM_NAME}_TEMPLATES_PATH', '')
        for path in dirarchy_templates_path.split(':'):
            if path:
                roots.append(Path(path))
        return roots

    @staticmethod
    def system_template_roots():
        roots = []
        platform_system = platform.system().strip().lower()
        match platform_system:
            case "windows":
                local_app_data_dpath = Path(os.environ['LOCALAPPDATA'])
                templates_dpath = local_app_data_dpath / f"{constants.LOWER_PROGRAM_NAME}/templates"
                templates_dpath.mkdir(parents=True, exist_ok=True)
                roots.append(templates_dpath)
                msystem_env_var = os.environ.get('MSYSTEM', None)
                if msystem_env_var == 'MINGW64' or msystem_env_var == 'MINGW32':
                    home_dpath = os.environ['HOME']
                    templates_dpath = Path(f"{home_dpath}/.local/share/{constants.LOWER_PROGRAM_NAME}/templates")
                    templates_dpath.mkdir(parents=True, exist_ok=True)
                    roots.append(templates_dpath)
            case "linux":
                home_dpath = os.environ['HOME']
                templates_dpath = Path(f"{home_dpath}/.local/share/{constants.LOWER_PROGRAM_NAME}/templates")
                templates_dpath.mkdir(parents=True, exist_ok=True)
                roots.append(templates_dpath)
            case _:
                raise Exception(f"System not handled: '{platform_system}'")
        return roots

    def __treat_file_node(self, file_node: XMLTree.Element, working_dir: Path):
        template_fpath = file_node.attrib.get('template', None)
        if template_fpath is not None:
            print(f"<file  {template_fpath}>")
            template_fpath = self.__find_template(file_node, template_fpath)
            working_dir = self.__treat_xml_file(template_fpath, working_dir, "file")
        else:
            filepath = self.__fsys_node_path(file_node)
            print(f"<file {working_dir}/ {filepath}>")
            assert 'template' not in file_node.attrib
            file_dir = Path(filepath).parent
            working_dir /= file_dir
            working_dir.mkdir(parents=True, exist_ok=True)
            with open(f"{working_dir}/{filepath.name}", "w") as file:
                file.write(f"{self.__file_text(file_node)}")
        return working_dir

    def __file_text(self, file_node: XMLTree.Element):
        copy_attr = file_node.attrib.get('copy')
        if copy_attr is None:
            text: str = "" if file_node.text is None else self.__strip_text(file_node.text)
        else:
            copy_attr = self.__format_str(copy_attr)
            with open(copy_attr) as copied_file:
                text: str = copied_file.read()
        format_attr = file_node.attrib.get('format')
        if format_attr is None:
            format_attr = "format"
        else:
            format_attr = self.__format_str(format_attr)
        format_attr_list: list = format_attr.split('|')
        if not format_attr_list or "raw" in format_attr_list:
            return text
        if "format" in format_attr_list:
            text = self.__format_str(text)
        elif "super_format" in format_attr_list:
            text = self.__super_format_str(text)
        return text

    def __treat_if_node(self, if_node: XMLTree.Element, working_dir: Path):
        from re import match, fullmatch
        then_nodes = if_node.findall('then')
        else_nodes = if_node.findall('else')
        then_count = len(then_nodes)
        else_count = len(else_nodes)
        if then_count > 1:
            raise Exception("Too many 'then' nodes for a 'if' node.")
        if else_count > 1:
            raise Exception("Too many 'else' nodes for a 'if' node.")
        if else_count and then_count == 0:
            raise Exception("A 'else' node is provided for a 'if' node but a 'then' node is missing.")
        expr_attr = if_node.attrib['expr']
        expr_attr = self.__format_str(expr_attr)
        b_expr = eval(expr_attr)
        if b_expr:
            if then_count == 0:
                self.__treat_action_children_nodes_of(if_node, working_dir)
            else:
                self.__treat_action_children_nodes_of(then_nodes[0], working_dir)
        elif else_count > 0:
            self.__treat_action_children_nodes_of(else_nodes[0], working_dir)
        return working_dir

    def __treat_action_children_nodes_of(self, node, working_dir):
        for child_node in node:
            self.__treat_action_node(child_node, working_dir)

    def __treat_match_node(self, match_node: XMLTree.Element, working_dir: Path):
        expr_attr = match_node.attrib['expr']
        expr_attr = self.__format_str(expr_attr)
        assert match_node.text is None or len(match_node.text.strip()) == 0
        found_case_node = None
        default_case_node = None
        if len(match_node) == 0:
            raise Exception("case nodes are missing in match node.")
        for case_node in match_node:
            assert case_node.tag == "case"
            case_value = case_node.attrib.get('value', None)
            if case_value is not None:
                if expr_attr == self.__format_str(case_value):
                    found_case_node = case_node
                    break
                continue
            case_expr = case_node.attrib.get('expr', None)
            if case_expr is not None:
                if re.fullmatch(self.__format_str(case_expr), expr_attr):
                    found_case_node = case_node
                    break
                continue
            if default_case_node is not None:
                raise Exception(f"A match node cannot have two default case nodes.")
            default_case_node = case_node
        if found_case_node:
            self.__treat_action_children_nodes_of(found_case_node, working_dir)
        elif default_case_node:
            self.__treat_action_children_nodes_of(default_case_node, working_dir)
        return working_dir

    def __format_str(self, text: str):
        neo_text: str = ""
        for line in io.StringIO(text):
            neo_text += line.format_map(self.__variables)
        return neo_text

    def __super_format_str(self, text: str):
        neo_text: str = ""
        for line in io.StringIO(text):
            index = 0
            neo_line = ""
            for mre in re.finditer(self.VAR_REGEX, line):
                if mre.group(self.SKIP_GROUP_ID):
                    neo_line += line[index:mre.start(self.SKIP_GROUP_ID)] + mre.group(self.SKIP_GROUP_ID)[0]
                    index = mre.end(self.SKIP_GROUP_ID)
                    continue
                var_name = mre.group(self.VAR_NAME_GROUP_ID)
                neo_line += line[index:mre.start(0)]
                index = mre.end(0)
                if var_name not in self.__variables:
                    raise Exception(f"Variable not set: '{var_name}'!")
                neo_line += self.__variables[var_name]
                # print(f"Var: {var_name} = '{self.__variables[var_name]}'")
            neo_line += line[index:]
            neo_text += neo_line
        return neo_text

    def __strip_text(self, text):
        text = text.lstrip()
        if len(text) > 0:
            idx = 0
            while " \t".find(text[-(idx + 1)]) != -1:
                idx = idx + 1
            if idx > 0:
                text = text[:-idx + 1]
        return text

    def __fsys_node_path(self, fsys_node):
        dir_path_str = fsys_node.attrib['path']
        dir_path_str = self.__format_str(dir_path_str)
        dir_path = Path(dir_path_str)
        return dir_path

    def __treat_root_node(self, dirarchy_node: XMLTree.Element, working_dir, expect):
        if dirarchy_node.tag != constants.ROOT_NODE_NAME:
            raise RuntimeError(f"Root node must be '{constants.ROOT_NODE_NAME}'!")
        self.__treat_vars_node(dirarchy_node.find("vars"))
        dir_nodes = dirarchy_node.findall("dir")
        fsys_node = dir_nodes[0] if len(dir_nodes) > 0 else None
        if fsys_node is None:
            if expect == "dir":
                raise Exception("Directory template was expected!")
            file_nodes = dirarchy_node.findall("file")
            fsys_node = file_nodes[0] if len(file_nodes) > 0 else None
            if fsys_node is None and expect == "file":
                raise Exception("File template was expected!")
        return self.__treat_action_node(fsys_node, working_dir)

    def __treat_vars_node(self, vars_node: XMLTree.Element):
        if vars_node is None:
            return
        for var_node in vars_node.iterfind("var"):
            self.__treat_var_node(var_node)

    def __treat_var_node(self, var_node: XMLTree.Element):
        var_name = var_node.attrib.get('name')
        if not re.match(self.VAR_NAME_REGEX, var_name):
            raise Exception(f"Variable name is not a valid name: '{var_name}'.")
        if var_name not in self.__variables:
            var_value = var_node.attrib.get('value', None)
            if var_value is not None:
                var_value = self.__format_str(var_value)
            else:
                var_rand_value = var_node.attrib.get('rand_value', None)
                if var_rand_value is not None:
                    var_value = self.generate_rand_value(var_rand_value)
                else:
                    var_type = var_node.attrib.get('type', 'str')
                    var_default = var_node.attrib.get('default', None)
                    var_restr = var_node.attrib.get('regex', None)
                    regex_full_match = RegexFullMatch(var_restr) if var_restr is not None else None
                    var_value = self.__ui.ask_valid_var(var_type, var_name, var_default, regex_full_match)
            self.__variables[var_name] = var_value
            # print(f"{var_name}:{var_type}({var_default})={var_value}")

    def generate_rand_value(self, var_rand_value: str):
        rmatch = re.fullmatch(r"(int|float|digit|alpha|lower|upper|alnum|snake_case|"
                              r"lower_sisy|upper_sisy|format_cvqd|'([ -~]+)'),\s*([!-~][ -~]*[!-~])\s*", var_rand_value)
        if not rmatch:
            raise Exception(f"Bad rand value: '{var_rand_value}'.")

        rand_category = rmatch.group(1)
        match rand_category:
            case 'int':
                return Dirarchy.__generate_rand_int(rmatch.group(3))
            case 'float':
                return Dirarchy.__generate_rand_float(rmatch.group(3))

        rand_params = rmatch.group(3)
        if rand_category == 'format_cvqd':
            p_match = re.fullmatch(r"\s*'([^abefghijklmnoprstuwxyzABEFGHIJKLMNOPRSTUWXYZ]+)'\s*",
                                   rand_params)
            if not p_match:
                raise Exception(f"String to format_cvqd is not a valid string: '{rand_params}'.")
            return random_string.random_format_cvqd_string(p_match.group(1))

        char_set = rmatch.group(2)
        min_len, max_len = [int(x) for x in rand_params.split(',')]
        match rand_category:
            case 'digit':
                return random_string.random_digit_string(min_len, max_len)
            case 'alpha':
                return random_string.random_alpha_string(min_len, max_len)
            case 'lower':
                return random_string.random_lower_string(min_len, max_len)
            case 'upper':
                return random_string.random_upper_string(min_len, max_len)
            case 'alnum':
                return random_string.random_alnum_string(min_len, max_len)
            case 'lower_sisy':
                return random_string.random_lower_sisy_string(min_len, max_len)
            case 'upper_sisy':
                return random_string.random_upper_sisy_string(min_len, max_len)
            case 'snake_case':
                return random_string.random_snake_case_string(min_len, max_len)
            case _:
                return random_string.random_string(char_set, min_len, max_len)

    @classmethod
    def __generate_rand_int(cls, params: str):
        rmatch = re.fullmatch(r'\s*([-+]?\d+)s*,\s*([-+]?\d+)\s*', params)
        if not rmatch:
            raise Exception(f"Bad rand int parameters: {params}. Two integers are expected: min, max.")
        min_value = int(rmatch.group(1))
        max_value = int(rmatch.group(2))
        return str(random.randint(min_value, max_value))

    @classmethod
    def __generate_rand_float(cls, params: str):
        rmatch = re.fullmatch(r'\s*([-+]?\d+(\.\d*)?)s*,\s*([-+]?\d+(\.\d*))\s*', params)
        if not rmatch:
            raise Exception(f"Bad rand int parameters: {params}. Two integers are expected: min, max.")
        min_value = float(rmatch.group(1))
        max_value = float(rmatch.group(3))
        return f"{random.uniform(min_value, max_value):.3f}"

    def __current_source_dir(self):
        return self.__source_file_stack[-1]

    def __treat_xml_file(self, dirarchy_fpath, working_dir, expect):
        assert expect is None or expect == "dir" or expect == "file"
        print('#' * 80)
        dirarchy_fpath = Path(dirarchy_fpath)
        print(f"Input file: {dirarchy_fpath}")
        with open(dirarchy_fpath, 'r') as dirarchy_file:
            tree = XMLTree.parse(dirarchy_file)
            self.__source_file_stack.append(dirarchy_fpath.absolute().parent)
            self.__variables['$CURRENT_SOURCE_DIR'] = self.__current_source_dir()
            try:
                return self.__treat_root_node(tree.getroot(), working_dir, expect)
            finally:
                self.__source_file_stack.pop(-1)
                if len(self.__source_file_stack) > 0:
                    self.__variables['$CURRENT_SOURCE_DIR'] = self.__current_source_dir()

    def treat_xml_file(self, dirarchy_fpath, working_dir=Path.cwd()):
        self.__treat_xml_file(dirarchy_fpath, working_dir, None)


if __name__ == '__main__':
    dirarchy = Dirarchy()
    dirarchy.run()
