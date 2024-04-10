import datetime
import os
from string import Formatter

from statement.abstract_statement import AbstractStatement


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
    TEMPLATE_DIR_VARNAME = '$TEMPLATE_DIR'

    def __init__(self, current_statement: AbstractStatement):
        self.__statement = current_statement

    def get_value(self, key, args, kwargs):
        if isinstance(key, str) and key[0] == '$':
            return self.__get_builtin_var_value(key)
        return super().get_value(key, args, kwargs)

    def __get_builtin_var_value(self, builtin_var_name):
        match builtin_var_name:
            case self.TEMPLATE_DIR_VARNAME:
                template_filepath = self.__statement.template_statement().template_filepath()
                return template_filepath.absolute().parent if template_filepath is not None else ""
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

