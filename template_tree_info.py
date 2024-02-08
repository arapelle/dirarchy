import io
import re
from enum import StrEnum
from pathlib import Path

import regex
from variables_dict import VariablesDict


class TemplateTreeInfo:
    class RootNodeType(StrEnum):
        FILE = "file"
        DIRECTORY = "dir"

    EXPECTED_ROOT_NODE_TYPE = "expected_root_node_type"
    PARENT = "parent"
    CURRENT_TEMGEN_FILEPATH = "current_temgen_filepath"
    CURRENT_DIRPATH = "current_dirpath"
    CURRENT_FILEPATH = "current_filepath"
    CURRENT_FILE = "current_file"
    VARIABLES = "variables"

    CURRENT_SOURCE_DIR_VARNAME = '$CURRENT_SOURCE_DIR'

    def __init__(self, **kwargs):
        # parent
        self.parent = None
        if self.PARENT in kwargs:
            self.parent = kwargs[self.PARENT]
        # expected_root_node_type
        self.expected_root_node_type = None
        if self.EXPECTED_ROOT_NODE_TYPE in kwargs:
            self.expected_root_node_type = kwargs[self.EXPECTED_ROOT_NODE_TYPE]
            assert self.PARENT in kwargs
            assert isinstance(self.expected_root_node_type, self.RootNodeType)
        else:
            self.expected_root_node_type = self.parent.expected_root_node_type if self.parent else None
        # current_temgen_filepath (and variables)
        if self.CURRENT_TEMGEN_FILEPATH in kwargs:
            self.current_temgen_filepath = kwargs[self.CURRENT_TEMGEN_FILEPATH]
            self.variables = VariablesDict(self.parent.variables.copy() if self.parent
                                           else kwargs.get(self.VARIABLES, {}))
        else:
            assert self.parent
            self.current_temgen_filepath = self.parent.current_temgen_filepath
            self.variables = self.parent.variables
        assert isinstance(self.current_temgen_filepath, Path)
        # current_dirpath
        if self.CURRENT_DIRPATH in kwargs:
            self.current_dirpath = kwargs[self.CURRENT_DIRPATH]
        else:
            self.current_dirpath = self.parent.current_dirpath if self.parent else Path.cwd()
        assert isinstance(self.current_dirpath, Path)
        # current_filepath
        if self.CURRENT_FILEPATH in kwargs:
            self.current_filepath = kwargs[self.CURRENT_FILEPATH]
        else:
            self.current_filepath = self.parent.current_filepath if self.parent else None
        assert self.current_filepath is None or isinstance(self.current_filepath, Path)
        # current_file
        if self.CURRENT_FILE in kwargs:
            self.current_file = kwargs[self.CURRENT_FILE]
        else:
            self.current_file = self.parent.current_file if self.parent else None
        # set built in variables
        self.__set_builtin_variables()

    def __set_builtin_variables(self):
        self.variables[self.CURRENT_SOURCE_DIR_VARNAME] = self.current_temgen_dirpath()

    def current_temgen_dirpath(self):
        return self.current_temgen_filepath.absolute().parent

    def format_str(self, value: str):
        formatted_value: str = ""
        for line in io.StringIO(value):
            formatted_value += line.format_map(self.variables)
        return formatted_value

    def super_format_str(self, value: str):
        formatted_value: str = ""
        for line in io.StringIO(value):
            index = 0
            formatted_line = ""
            for mre in re.finditer(regex.VAR_REGEX, line):
                if mre.group(regex.SKIP_GROUP_ID):
                    formatted_line += line[index:mre.start(regex.SKIP_GROUP_ID)] + mre.group(regex.SKIP_GROUP_ID)[0]
                    index = mre.end(regex.SKIP_GROUP_ID)
                    continue
                var_name = mre.group(regex.VAR_NAME_GROUP_ID)
                formatted_line += line[index:mre.start(0)]
                index = mre.end(0)
                if var_name not in self.variables:
                    raise Exception(f"Variable not set: '{var_name}'!")
                formatted_line += self.variables[var_name]
                # print(f"Var: {var_name} = '{self.__variables[var_name]}'")
            formatted_line += line[index:]
            formatted_value += formatted_line
        return formatted_value
