import xml.etree.ElementTree as XMLTree

import constants
import dir_node
import file_node
import vars_node
from execution_context import ExecutionContext
from template_tree_info import TemplateTreeInfo


class DirarchyNode:
    @staticmethod
    def treat_dirarchy_node(dirarchy_node: XMLTree.Element,
                            execution_context: ExecutionContext,
                            tree_info: TemplateTreeInfo):
        if dirarchy_node.tag != constants.ROOT_NODE_NAME:
            raise RuntimeError(f"Root node must be '{constants.ROOT_NODE_NAME}'!")
        vars_node.VarsNode.treat_vars_node(dirarchy_node.find("vars"), execution_context, tree_info)
        dir_nodes = dirarchy_node.findall("dir")
        fsys_node = dir_nodes[0] if len(dir_nodes) > 0 else None
        if fsys_node is None:
            if tree_info.expected_root_node_type == TemplateTreeInfo.RootNodeType.DIRECTORY:
                raise Exception("Directory template was expected!")
            file_nodes = dirarchy_node.findall("file")
            fsys_node = file_nodes[0] if len(file_nodes) > 0 else None
            if tree_info.expected_root_node_type == TemplateTreeInfo.RootNodeType.FILE:
                if fsys_node is None:
                    raise Exception("File template was expected!")
                elif len(file_nodes) > 1:
                    raise Exception("Only one 'file' node is expected at root.")
        elif len(dir_nodes) > 1 and tree_info.expected_root_node_type == TemplateTreeInfo.RootNodeType.DIRECTORY:
            raise Exception("Only one 'dir' node is expected at root.")
        match fsys_node.tag:
            case "dir":
                return dir_node.DirNode.treat_dir_node(fsys_node, execution_context, tree_info)
            case "file":
                return file_node.FileNode.treat_file_node(fsys_node, execution_context, tree_info)
            case _:
                assert False

    @staticmethod
    def treat_xml_file(execution_context: ExecutionContext,
                       tree_info: TemplateTreeInfo):
        print('#' * 80)
        print(f"Input file: {tree_info.current_temgen_filepath}")
        with open(tree_info.current_temgen_filepath, 'r') as dirarchy_file:
            tree = XMLTree.parse(dirarchy_file)
            return DirarchyNode.treat_dirarchy_node(tree.getroot(), execution_context, tree_info)
