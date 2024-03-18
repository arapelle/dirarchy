import xml.etree.ElementTree as XMLTree
from abc import abstractmethod
from pathlib import Path

from statement.abstract_statement import AbstractStatement
from statement.abstract_main_statement import AbstractMainStatement


class AbstractDirStatement(AbstractMainStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, **kargs):
        super().__init__(current_node, parent_statement, **kargs)

    @abstractmethod
    def current_output_dirpath(self) -> Path:
        pass

    def current_dir_statement(self):
        return self
