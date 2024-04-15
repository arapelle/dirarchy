import xml.etree.ElementTree as XMLTree

from statement.abstract_branch_statement import AbstractBranchStatement
from statement.abstract_statement import AbstractStatement


class IfStatement(AbstractBranchStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, **kargs):
        super().__init__(current_node, parent_statement, **kargs)

    def allows_template(self):
        return True

    def execute(self):
        from re import match, fullmatch
        then_node = None
        else_node = None
        unknown_children_count = 0
        for child_node in self.current_node():
            match child_node.tag:
                case "then":
                    if then_node is None:
                        then_node = child_node
                    else:
                        raise RuntimeError("Too many 'then' nodes for a 'if' node.")
                case "else":
                    if else_node is None:
                        else_node = child_node
                    else:
                        raise RuntimeError("Too many 'else' nodes for a 'if' node.")
                case _:
                    unknown_children_count += 1
        if else_node is not None and then_node is None:
            raise RuntimeError("A 'else' node is provided for a 'if' node but a 'then' node is missing.")
        if unknown_children_count > 0 and then_node is not None:
            raise RuntimeError(f"In 'if', bad child node type: {child_node.tag}.")
        expr_attr = self.current_node().attrib['expr']
        expr_attr = self.format_str(expr_attr)
        bool_expr_value = bool(eval(expr_attr))
        if bool_expr_value:
            if then_node is None:
                self.current_main_statement().treat_children_nodes_of(self.current_node())
            else:
                self.current_main_statement().treat_children_nodes_of(then_node)
        elif else_node is not None:
            self.current_main_statement().treat_children_nodes_of(else_node)

    def check_not_template_attributes(self, nb_template_attributes: int):
        if "expr" in self.current_node().attrib:
            raise RuntimeError(f"The attribute 'expr' is unexpected when calling a 'if' template.")

    def post_template_run(self, template_statement):
        if len(self.current_node()) > 0:
            raise RuntimeError("No child statement is expected when calling a 'if' template.")
