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

    def treat_child_node(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        match child_node.tag:
            case "dir":
                dir_statement = self._create_dir_statement(node, child_node, current_statement)
                dir_statement.run()
            case "file":
                file_statement = self._create_file_statement(node, child_node, current_statement)
                file_statement.run()
            case "exec":
                exec_statement = self._create_exec_statement(node, child_node, current_statement)
                exec_statement.run()
            case "if":
                if_statement = self._create_if_statement(node, child_node, current_statement)
                if_statement.run()
            case "match":
                match_statement = self._create_match_statement(node, child_node, current_statement)
                match_statement.run()
            case "block":
                block_statement = self._create_block_statement(node, child_node, current_statement)
                block_statement.run()
            case "vars":
                vars_statement = self._create_vars_statement(node, child_node, current_statement)
                vars_statement.run()
            case "var":
                var_statement = self._create_var_statement(node, child_node, current_statement)
                var_statement.run()
            case _:
                super().treat_child_node(node, child_node, current_statement)

    def _create_dir_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        from statement.dir_statement import DirStatement
        return DirStatement(child_node, current_statement)

    def _create_file_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        from statement.file_statement import FileStatement
        return FileStatement(child_node, current_statement)

    def _create_exec_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        from statement.exec_statement import ExecStatement
        return ExecStatement(child_node, current_statement)

    def _create_if_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        from statement.if_statement import IfStatement
        return IfStatement(child_node, current_statement)

    def _create_match_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        from statement.match_statement import MatchStatement
        return MatchStatement(child_node, current_statement)

    def _create_block_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        from statement.block_statement import BlockStatement
        return BlockStatement(child_node, current_statement)

    def _create_vars_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        from statement.vars_statement import VarsStatement
        return VarsStatement(child_node, current_statement)

    def _create_var_statement(self, node: XMLTree.Element, child_node: XMLTree.Element, current_statement):
        from statement.var_statement import VarStatement
        return VarStatement(child_node, current_statement)
