from enum import StrEnum
from pathlib import Path

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
        # current_filepath
        if self.CURRENT_FILEPATH in kwargs:
            self.current_filepath = kwargs[self.CURRENT_FILEPATH]
        else:
            self.current_filepath = self.parent.current_filepath if self.parent else None
        # current_file
        if self.CURRENT_FILE in kwargs:
            self.current_file = kwargs[self.CURRENT_FILE]
        else:
            self.current_file = self.parent.current_file if self.parent else None

    def current_temgen_dirpath(self):
        return self.current_temgen_filepath.absolute().parent
