import os
import re
import glob
import platform
from pathlib import Path

import constants
import regex
from ask_dialog import AskDialog
from variables_dict import VariablesDict


def environment_template_roots():
    roots = []
    dirarchy_templates_path = os.environ.get(f'{constants.UPPER_PROGRAM_NAME}_TEMPLATES_PATH', '')
    for path in dirarchy_templates_path.split(':'):
        if path:
            roots.append(Path(path))
    return roots


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


def global_template_roots():
    roots = []
    roots.extend(system_template_roots())
    roots.extend(environment_template_roots())
    return roots


class ExecutionContext:
    def __init__(self, ui: AskDialog, variables: VariablesDict):
        self.__ui = ui
        self.__variables = variables
        self.__template_root_dpaths = global_template_roots()
        self.__template_root_dpaths.append(Path("."))

    @property
    def ui(self):
        return self.__ui

    @property
    def init_variables(self):
        return self.__variables

    @property
    def template_roots(self):
        return self.__template_root_dpaths

    def find_template(self, template_fpath: Path, version_attr):
        template_dpath = template_fpath.parent
        template_fname = template_fpath.name
        rmatch = re.fullmatch(regex.TEMPLATE_FILENAME_REGEX, template_fname)
        if not rmatch:
            raise RuntimeError(f"The path '{template_fpath}' is not a valid path.")
        template_name = rmatch.group(regex.TEMPLATE_FILENAME_REGEX_NAME_GROUP_ID)
        template_ext = rmatch.group(regex.TEMPLATE_FILENAME_REGEX_EXT_GROUP_ID)
        if template_ext is not None:
            if version_attr:
                print("WARNING: The attribute version is ignored as the provided template is a file path "
                      f"(version or extension is contained in the path): '{template_fpath}'.")
            for template_root_dpath in self.__template_root_dpaths:
                xml_path = template_root_dpath / template_fpath
                if xml_path.exists():
                    return xml_path
            raise RuntimeError(f"Template not found: '{template_fpath}'.")
        template_version = rmatch.group(regex.TEMPLATE_FILENAME_REGEX_VERSION_GROUP_ID)
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
        for template_root_dpath in self.__template_root_dpaths:
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

