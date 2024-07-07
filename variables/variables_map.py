import datetime
import tempfile
from pathlib import Path
from typing import Mapping

from statement.abstract_statement import AbstractStatement
from variables.builtin import BuiltinTemgenVersion, BuiltinDate, BuiltinTime, BuiltinStrftime, BuiltinEnv, BuiltinEval, \
    BuiltinJoin


class VariablesMap(Mapping):
    def __init__(self, current_statement: AbstractStatement, is_eval_context: bool):
        self.__statement = current_statement
        self.__is_eval_context = is_eval_context

    def __getitem__(self, var_name):
        if isinstance(var_name, str) and var_name[0] == '$':
            return self.__get_builtin_var_value(var_name)
        return self.__get_var_value(var_name)

    def __len__(self):
        assert False

    def __iter__(self):
        assert False

    def __get_var_value(self, var_name):
        statement = self.__statement
        while statement is not None:
            value = statement.variables().get(var_name, None)
            if value is not None:
                return value
            statement = statement.parent_statement()
        raise KeyError(var_name)

    def __get_builtin_var_value(self, builtin_var_name):
        match builtin_var_name:
            case "$TEMGEN_VERSION":
                return BuiltinTemgenVersion(self.__is_eval_context)
            case "$TMP":
                return tempfile.gettempdir()
            case "$CURRENT_WORKING_DIR":
                return Path.cwd().as_posix()
            case "$TEMPLATE_DIR":
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
            case "$EVAL":
                return BuiltinEval()
            case "$JOIN":
                return BuiltinJoin()
            case "$JOIN_KEEP_EMPTY":
                return BuiltinJoin(skip_empty=False)
            case _:
                raise KeyError(builtin_var_name)
