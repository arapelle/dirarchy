import datetime
from typing import Mapping

from variables.variables_dict import VariablesDict
from statement.abstract_statement import AbstractStatement


class VariablesMap(Mapping):
    def __init__(self, current_statement: AbstractStatement):
        self.__statement = current_statement

    def __getitem__(self, var_name):
        statement = self.__statement
        while statement is not None:
            value = statement.variables().get(var_name, None)
            if value is not None:
                return value
            statement = statement.parent_statement()
        raise KeyError(var_name)

    def __len__(self):
        assert False

    def __iter__(self):
        assert False
