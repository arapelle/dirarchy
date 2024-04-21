import xml.etree.ElementTree as XMLTree
from abc import ABC
from typing import final

from util.log import MethodScopeLog
from statement.abstract_statement import AbstractStatement


class AbstractMainStatement(AbstractStatement, ABC):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, **kargs):
        super().__init__(current_node, parent_statement, **kargs)
        self.__children_treated = False

    @final
    def run(self):
        with MethodScopeLog(self):
            super()._run()
            if not self.__children_treated:
                self.treat_children_nodes()

    def current_main_statement(self):
        return self

    def treat_children_nodes(self):
        self.treat_children_nodes_of(self.current_node())
        self.__children_treated = True

    def extends_template(self):
        return False

    @final
    def treat_children_nodes_of(self, node: XMLTree.Element):
        self.check_number_of_children_nodes_of(node)
        if len(node) == 0:
            if not self.was_template_called() or self.extends_template():
                self.treat_text_of(node)
            elif not self.is_node_text_empty(node):
                raise RuntimeError(f"Text is not expected when calling a template for '{node.tag}'.")
        else:
            if not self.was_template_called() or self.extends_template():
                for child_node in node:
                    self.treat_child_node(node, child_node)
            else:
                raise RuntimeError(f"Children statements are not expected when calling a template for '{node.tag}'.")

    def check_number_of_children_nodes_of(self, node: XMLTree.Element):
        pass

    def treat_text_of(self, node: XMLTree.Element):
        if not self.is_node_text_empty(node):
            raise RuntimeError(f"In '{node.tag}', text is expected to be empty.")

    def treat_child_node(self, node: XMLTree.Element, child_node: XMLTree.Element):
        raise RuntimeError(f"In '{node.tag}', bad child node type: {child_node.tag}.")
