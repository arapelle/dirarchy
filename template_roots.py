import os
from pathlib import Path

import constants
import platform


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


def template_roots():
    roots = []
    roots.extend(global_template_roots())
    roots.append(Path("."))
    return roots
