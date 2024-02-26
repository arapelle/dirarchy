import xml.etree.ElementTree as XMLTree

from node import dir_node, file_node, if_node, match_node
from execution_context import ExecutionContext
from template_tree_info import TemplateTreeInfo


class NodeBase:
    @staticmethod
    def treat_action_node(node: XMLTree.Element,
                          execution_context: ExecutionContext,
                          tree_info: TemplateTreeInfo):
        assert node is not None
        match node.tag:
            case "dir":
                dir_node.DirNode.treat_dir_node(node, execution_context, tree_info)
            case "file":
                file_node.FileNode.treat_file_node(node, execution_context, tree_info)
            case "if":
                if_node.IfNode.treat_if_node(node, execution_context, tree_info)
            case "match":
                match_node.MatchNode.treat_match_node(node, execution_context, tree_info)
            case _:
                raise Exception(f"Unknown node type: {node.tag}.")

    @staticmethod
    def treat_action_children_nodes_of(node: XMLTree.Element,
                                       execution_context: ExecutionContext,
                                       tree_info: TemplateTreeInfo):
        for child_node in node:
            NodeBase.treat_action_node(child_node, execution_context, tree_info)

