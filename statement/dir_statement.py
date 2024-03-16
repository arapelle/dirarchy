import xml.etree.ElementTree as XMLTree
from builtins import RuntimeError
from pathlib import Path

from statement.abstract_dir_statement import AbstractDirStatement
from statement.abstract_statement import AbstractStatement


class DirStatement(AbstractDirStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, **kargs):
        super().__init__(current_node, parent_statement, **kargs)
        self.__output_dirpath = Path()

    def run(self):
        parent_output_dirpath = self.parent_statement().current_dir_statement().current_output_dirpath()
        self.__output_dirpath = parent_output_dirpath / self.format_str(self.current_node().attrib['path'])
        self.__output_dirpath.mkdir(parents=True, exist_ok=True)
        self.treat_children_nodes_of(self.current_node())

    def current_output_dirpath(self) -> Path:
        return self.__output_dirpath
