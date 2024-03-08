import xml.etree.ElementTree as XMLTree

import constants
from abstract_temgen import AbstractTemgen
from node import dir_node, file_node, vars_node
from template_tree_info import TemplateTreeInfo


class TemplateNode:
    @staticmethod
    def treat_template_node(template_node: XMLTree.Element,
                            temgen: AbstractTemgen,
                            tree_info: TemplateTreeInfo):
        if template_node.tag != constants.ROOT_NODE_NAME:
            raise RuntimeError(f"Root node must be '{constants.ROOT_NODE_NAME}'!")
        variables_node = template_node.find("vars")
        if variables_node is not None:
            vars_node.VarsNode.treat_vars_node(variables_node, temgen, tree_info)
        dir_nodes = template_node.findall("dir")
        fsys_node = dir_nodes[0] if len(dir_nodes) > 0 else None
        if fsys_node is None:
            if tree_info.expected_root_node_type == TemplateTreeInfo.RootNodeType.DIRECTORY:
                raise Exception("Directory template was expected!")
            file_nodes = template_node.findall("file")
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
                return dir_node.DirNode.treat_dir_node(fsys_node, temgen, tree_info)
            case "file":
                return file_node.FileNode.treat_file_node(fsys_node, temgen, tree_info)
            case _:
                assert False
