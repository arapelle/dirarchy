import re
import xml.etree.ElementTree as XMLTree

from execution_context import ExecutionContext
import node_base
from template_tree_info import TemplateTreeInfo


class MatchNode:
    @staticmethod
    def treat_match_node(match_node: XMLTree.Element,
                         execution_context: ExecutionContext,
                         tree_info: TemplateTreeInfo):
        expr_attr = match_node.attrib['expr']
        expr_attr = tree_info.format_str(expr_attr)
        assert match_node.text is None or len(match_node.text.strip()) == 0
        found_case_node = None
        default_case_node = None
        if len(match_node) == 0:
            raise Exception("case nodes are missing in match node.")
        for case_node in match_node:
            assert case_node.tag == "case"
            case_value = case_node.attrib.get('value', None)
            if case_value is not None:
                if expr_attr == tree_info.format_str(case_value):
                    found_case_node = case_node
                    break
                continue
            case_expr = case_node.attrib.get('expr', None)
            if case_expr is not None:
                if re.fullmatch(tree_info.format_str(case_expr), expr_attr):
                    found_case_node = case_node
                    break
                continue
            if default_case_node is not None:
                raise Exception(f"A match node cannot have two default case nodes.")
            default_case_node = case_node
        if found_case_node:
            node_base.NodeBase.treat_action_children_nodes_of(found_case_node, execution_context, tree_info)
        elif default_case_node:
            node_base.NodeBase.treat_action_children_nodes_of(default_case_node, execution_context, tree_info)
