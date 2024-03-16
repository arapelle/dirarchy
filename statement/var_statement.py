import xml.etree.ElementTree as XMLTree
from builtins import RuntimeError

from statement.abstract_statement import AbstractStatement
from statement.abstract_main_statement import AbstractMainStatement


class VarStatement(AbstractMainStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, **kargs):
        super().__init__(current_node, parent_statement, variables=parent_statement.variables(), **kargs)

    def run(self):
        #TODO Treat current_node() attributes and construct a variable to self.variables().
        self.treat_children_nodes_of(self.current_node())

    def treat_children_nodes_of(self, node: XMLTree.Element):
        if len(node) > 1:
            raise RuntimeError(f"Too many nodes for <{node.tag}>.")
        super().treat_child_node(node, node[0])

    def treat_child_node(self, node: XMLTree.Element, child_node: XMLTree.Element):
        match child_node.tag:
            case "random":
                assert False
                # TODO match: <random>
                # random_statement = RandomStatement(child_node, self)
                # random_statement.run()
            case _:
                raise RuntimeError(f"In {node.tag}, unknown child node type: {child_node.tag}.")
