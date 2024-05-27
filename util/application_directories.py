import os
import platform
import tempfile
from enum import IntFlag
from pathlib import Path


class ApplicationDirectories:
    class PlatformMode(IntFlag):
        WINDOWS_ONLY = 1
        LINUX_ONLY = 2
        DEFAULT = WINDOWS_ONLY | LINUX_ONLY

    def __init__(self, app_name: str, platform_mode=PlatformMode.DEFAULT):
        self.__platform_mode = platform_mode
        self.__app_name = app_name
        platform_system = platform.system().strip().lower()
        self.__data_dirpaths = []
        match platform_system:
            case "windows":
                msystem_env_var = os.environ.get('MSYSTEM', None)
                match msystem_env_var:
                    case 'MINGW64' | 'MINGW32' | 'MSYS':
                        if platform_mode & self.PlatformMode.LINUX_ONLY:
                            self.__settings_dirpath = self.__linux_settings_dirpath() / self.__app_name
                        if platform_mode & self.PlatformMode.WINDOWS_ONLY:
                            self.__data_dirpaths.append(self.__windows_settings_dirpath() / self.__app_name)
                    case _:
                        assert platform_mode & self.PlatformMode.WINDOWS_ONLY
                        self.__settings_dirpath = self.__windows_settings_dirpath() / self.__app_name
            case "linux":
                assert platform_mode & self.PlatformMode.LINUX_ONLY
                self.__settings_dirpath = self.__linux_settings_dirpath() / self.__app_name
            case _:
                raise Exception(f"System not handled: '{platform_system}'")
        self.__data_dirpaths.append(self.__settings_dirpath)

    def settings_dirpath(self):
        return self.__settings_dirpath

    def system_data_dirpaths(self, data_dirname: str):
        return [data_dir_path / data_dirname for data_dir_path in self.__data_dirpaths]

    def main_system_data_dirpath(self, data_dirname: str):
        return self.__data_dirpaths[0] / data_dirname

    def env_data_dirpaths(self, data_dirname: str):
        upper_app_name = self.__app_name.upper().replace('-', '_')
        # TODO: Use https://inflection.readthedocs.io/en/latest/#inflection.underscore
        data_dirpaths = os.environ.get(f'{upper_app_name}_{data_dirname}_PATH', '')
        dirs = []
        for path in data_dirpaths.split(':'):
            if len(path) > 0:
                dirs.append(path)
        return dirs

    def data_dirpaths(self, data_dirname: str):
        dirs = []
        dirs.extend(self.system_data_dirpaths(data_dirname))
        dirs.extend(self.env_data_dirpaths(data_dirname))
        return dirs

    def tmp_dirpath(self):
        return Path(tempfile.gettempdir()) / self.__app_name

    def log_dirpath(self):
        return self.tmp_dirpath() / "log"

    @staticmethod
    def __windows_settings_dirpath() -> Path:
        return Path(os.environ['LOCALAPPDATA'])

    @staticmethod
    def __linux_settings_dirpath() -> Path:
        return Path(f"{os.environ['HOME']}/.local/share/")
