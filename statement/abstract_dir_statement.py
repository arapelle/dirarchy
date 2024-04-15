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

    def treat_child_node(self, node: XMLTree.Element, child_node: XMLTree.Element):
        match child_node.tag:
            case "dir":
                dir_statement = self._create_dir_statement(node, child_node)
                dir_statement.run()
            case "file":
                file_statement = self._create_file_statement(node, child_node)
                file_statement.run()
            case "if":
                if_statement = self._create_if_statement(node, child_node)
                if_statement.run()
            case "match":
                match_statement = self._create_match_statement(node, child_node)
                match_statement.run()
            case _:
                super().treat_child_node(node, child_node)

    def _create_dir_statement(self, node: XMLTree.Element, child_node: XMLTree.Element):
        from statement.dir_statement import DirStatement
        return DirStatement(child_node, self)

    def _create_file_statement(self, node: XMLTree.Element, child_node: XMLTree.Element):
        from statement.file_statement import FileStatement
        return FileStatement(child_node, self)

    def _create_if_statement(self, node: XMLTree.Element, child_node: XMLTree.Element):
        from statement.if_statement import IfStatement
        return IfStatement(child_node, self)

    def _create_match_statement(self, node: XMLTree.Element, child_node: XMLTree.Element):
        from statement.match_statement import MatchStatement
        return MatchStatement(child_node, self)
