import xml.etree.ElementTree as XMLTree
from abc import abstractmethod, ABC

from statement.abstract_statement import AbstractStatement


class AbstractMainStatement(AbstractStatement, ABC):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, **kargs):
        super().__init__(current_node, parent_statement, **kargs)

    def treat_children_nodes_of(self, node: XMLTree.Element):
        for child_node in node:
            self.treat_child_node(node, child_node)

    def treat_child_node(self, node: XMLTree.Element, child_node: XMLTree.Element):
        raise RuntimeError(f"In '{node.tag}', bad child node type: {child_node.tag}.")

    def current_main_statement(self):
        return self
