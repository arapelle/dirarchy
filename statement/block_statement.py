import xml.etree.ElementTree as XMLTree

from statement.abstract_branch_statement import AbstractBranchStatement
from statement.abstract_statement import AbstractStatement


class BlockStatement(AbstractBranchStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, **kargs):
        super().__init__(current_node, parent_statement, **kargs)

    def allows_template(self):
        return True

    def execute(self):
        self.current_main_statement().treat_children_nodes_of(self.current_node(), self)

    def post_template_run(self, template_statement):
        self.current_main_statement().treat_children_nodes_of(self.current_node(), self)
