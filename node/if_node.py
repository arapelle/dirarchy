import xml.etree.ElementTree as XMLTree

from execution_context import ExecutionContext
from node import node_base
from template_tree_info import TemplateTreeInfo


class IfNode:
    @staticmethod
    def treat_if_node(if_node: XMLTree.Element,
                      execution_context: ExecutionContext,
                      tree_info: TemplateTreeInfo):
        from re import match, fullmatch
        then_nodes = if_node.findall('then')
        else_nodes = if_node.findall('else')
        then_count = len(then_nodes)
        else_count = len(else_nodes)
        if then_count > 1:
            raise Exception("Too many 'then' nodes for a 'if' node.")
        if else_count > 1:
            raise Exception("Too many 'else' nodes for a 'if' node.")
        if else_count and then_count == 0:
            raise Exception("A 'else' node is provided for a 'if' node but a 'then' node is missing.")
        expr_attr = if_node.attrib['expr']
        expr_attr = tree_info.format_str(expr_attr)
        b_expr = eval(expr_attr)
        if b_expr:
            if then_count == 0:
                node_base.NodeBase.treat_action_children_nodes_of(if_node, execution_context, tree_info)
            else:
                node_base.NodeBase.treat_action_children_nodes_of(then_nodes[0], execution_context, tree_info)
        elif else_count > 0:
            node_base.NodeBase.treat_action_children_nodes_of(else_nodes[0], execution_context, tree_info)
