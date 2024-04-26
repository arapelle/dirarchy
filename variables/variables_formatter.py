import datetime
import os
import tempfile
from pathlib import Path
from string import Formatter


class BuiltinDate:
    def __format__(self, format_spec):
        assert isinstance(format_spec, str)
        today = datetime.date.today()
        return f"{today.year}{format_spec}{today.month:02}{format_spec}{today.day:02}"


class BuiltinTime:
    def __format__(self, format_spec):
        assert isinstance(format_spec, str)
        now = datetime.datetime.now()
        return f"{now.hour:02}{format_spec}{now.minute:02}{format_spec}{now.second:02}"


class BuiltinStrftime:
    def __format__(self, format_spec):
        assert isinstance(format_spec, str)
        return datetime.datetime.now().strftime(format_spec)


class BuiltinEnv:
    def __format__(self, format_spec):
        assert isinstance(format_spec, str)
        return os.environ[format_spec]


class VariablesFormatter(Formatter):
    from statement.abstract_statement import AbstractStatement

    TEMPLATE_DIR_VARNAME = '$TEMPLATE_DIR'

    def __init__(self, current_statement: AbstractStatement):
        self.__statement = current_statement

    def get_value(self, key, args, kwargs):
        if isinstance(key, str) and key[0] == '$':
            return self.__get_builtin_var_value(key)
        return super().get_value(key, args, kwargs)

    def __get_builtin_var_value(self, builtin_var_name):
        match builtin_var_name:
            case "$TMP":
                return tempfile.gettempdir()
            case "$CURRENT_WORKING_DIR":
                return Path.cwd().as_posix()
            case self.TEMPLATE_DIR_VARNAME:
                template_filepath = self.__statement.template_statement().template_filepath()
                return template_filepath.absolute().parent.as_posix() if template_filepath is not None else ""
            case "$ROOT_TEMPLATE_DIR":
                root_template_statement = self.__statement.template_statement().root_parent_template_statement()
                template_filepath = root_template_statement.template_filepath()
                return template_filepath.absolute().parent.as_posix() if template_filepath is not None else ""
            case "$ROOT_OUTPUT_DIR":
                root_template_statement = self.__statement.template_statement().root_parent_template_statement()
                return root_template_statement.current_output_dirpath().as_posix()
            case "$LOCAL_ROOT_OUTPUT_DIR":
                template_statement = self.__statement.template_statement()
                return template_statement.current_output_dirpath().as_posix()
            case "$TREE_ROOT_OUTPUT_DIR":
                dir_statement = self.__statement.tree_root_dir_statement()
                return dir_statement.current_output_dirpath().as_posix() if dir_statement is not None else ""
            case "$LOCAL_TREE_ROOT_OUTPUT_DIR":
                dir_statement = self.__statement.local_tree_root_dir_statement()
                return dir_statement.current_output_dirpath().as_posix() if dir_statement is not None else ""
            case "$OUTPUT_DIR":
                file_statement = self.__statement.current_file_statement()
                if file_statement is not None:
                    return file_statement.current_output_filepath().parent.as_posix()
                dir_statement = self.__statement.current_dir_statement()
                assert dir_statement is not None
                return dir_statement.current_output_dirpath().as_posix()
            case "$OUTPUT_FILE":
                file_statement = self.__statement.current_file_statement()
                assert file_statement is not None
                return file_statement.current_output_filepath().as_posix()
            case "$OUTPUT_FILE_NAME":
                file_statement = self.__statement.current_file_statement()
                assert file_statement is not None
                return file_statement.current_output_filepath().name
            case "$OUTPUT_FILE_STEM":
                file_statement = self.__statement.current_file_statement()
                assert file_statement is not None
                return file_statement.current_output_filepath().stem
            case "$OUTPUT_FILE_EXT":
                file_statement = self.__statement.current_file_statement()
                assert file_statement is not None
                return file_statement.current_output_filepath().suffix
            case "$OUTPUT_FILE_EXTS":
                file_statement = self.__statement.current_file_statement()
                assert file_statement is not None
                return "".join(file_statement.current_output_filepath().suffixes)
            case "$YEAR":
                return f"{datetime.date.today().year}"
            case "$MONTH":
                return f"{datetime.date.today().month:02}"
            case "$DAY":
                return f"{datetime.date.today().day:02}"
            case "$DATE":
                return BuiltinDate()
            case "$TIME":
                return BuiltinTime()
            case "$STRFTIME":
                return BuiltinStrftime()
            case "$ENV":
                return BuiltinEnv()
            case _:
                raise KeyError(builtin_var_name)
