import xml.etree.ElementTree as XMLTree
from abc import abstractmethod
from pathlib import Path

import constants
from statement.abstract_dir_statement import AbstractDirStatement
from statement.abstract_statement import AbstractStatement
from statement.vars_statement import VarsStatement


class TemplateStatement(AbstractDirStatement):
    from temgen import Temgen
    TEMGEN_LABEL = constants.LOWER_PROGRAM_NAME
    TEMPLATE_FILEPATH_LABEL = "template_filepath"
    OUTPUT_DIRPATH_LABEL = "output_dirpath"

    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, **kargs):
        if current_node.tag != constants.ROOT_NODE_NAME:
            raise RuntimeError(f"Root node must be '{constants.ROOT_NODE_NAME}'!")
        super().__init__(current_node, parent_statement, **kargs)
        if self.parent_statement() is not None:
            self.__parent_template_statement = self.parent_statement().template_statement()
            assert self.__parent_template_statement is not None
            self.__temgen = self.__parent_template_statement.temgen()
            self.__output_dirpath = self.parent_statement().current_dir_statement().current_output_dirpath()
        else:
            self.__parent_template_statement = None
            self.__temgen = kargs[TemplateStatement.TEMGEN_LABEL]
            self.__output_dirpath = kargs[TemplateStatement.OUTPUT_DIRPATH_LABEL]
        self.__template_filepath = Path(kargs.get(TemplateStatement.TEMPLATE_FILEPATH_LABEL))
        self.__current_child_statement = None

    def parent_template_statement(self):
        return self.__parent_template_statement

    def root_parent_template_statement(self):
        if self.__parent_template_statement is None:
            return self
        return self.__parent_template_statement.root_parent_template_statement()

    def temgen(self) -> Temgen:
        return self.__temgen

    def template_filepath(self):
        return self.__template_filepath

    def current_output_dirpath(self) -> Path:
        return self.__output_dirpath

    def current_child_statement(self):
        return self.__current_child_statement
