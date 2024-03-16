import xml.etree.ElementTree as XMLTree
from builtins import RuntimeError
from pathlib import Path

from statement.abstract_statement import AbstractStatement
from statement.abstract_main_statement import AbstractMainStatement


class FileStatement(AbstractMainStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractMainStatement, **kargs):
        super().__init__(current_node, parent_statement, **kargs)
        self.__output_filepath = Path()
        self.__output_file = None

    def current_file_statement(self):
        return self

    def current_output_filepath(self):
        return self.__output_filepath

    def current_output_file(self):
        return self.__output_file

    def run(self):
        parent_output_dirpath = self.parent_statement().current_dir_statement().current_output_dirpath()
        self.__output_filepath = Path(parent_output_dirpath / self.format_str(self.current_node().attrib['path']))
        self.__output_filepath.parent.mkdir(parents=True, exist_ok=True)
        open_mode = "w"
        with open(self.__output_filepath, open_mode) as file:
            self.__output_file = file
            self.treat_children_nodes_of(self.current_node())
        self.__output_file = None

    def treat_child_node(self, node: XMLTree.Element, child_node: XMLTree.Element):
        super().treat_child_node(node, child_node)
        # TODO match: <contents>
