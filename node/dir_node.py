import xml.etree.ElementTree as XMLTree
from pathlib import Path

import temgen
from execution_context import ExecutionContext
from node import node_base
from template_tree_info import TemplateTreeInfo


class DirNode:
    @staticmethod
    def treat_dir_node(dir_node: XMLTree.Element,
                       execution_context: ExecutionContext,
                       tree_info: TemplateTreeInfo):
        template_path = dir_node.attrib.get('template', None)
        if template_path is not None:
            print(f"<dir  {template_path}>")
            assert 'path' not in dir_node.attrib
            template_path = Path(tree_info.format_str(template_path))
            version_attr = dir_node.attrib.get('template-version', None)
            if version_attr:
                version_attr = tree_info.format_str(version_attr)
            template_path = execution_context.find_template_file(template_path, version_attr)
            template_tree_info = TemplateTreeInfo(parent=tree_info,
                                                  expected_root_node_type=TemplateTreeInfo.RootNodeType.DIRECTORY,
                                                  current_template_filepath=Path(template_path))
            working_dir = temgen.Temgen.treat_template_tree_info(execution_context, template_tree_info)
            dir_tree_info = TemplateTreeInfo(parent=tree_info, current_dirpath=working_dir)
            dir_tree_info.variables = template_tree_info.variables
        else:
            dir_path = Path(tree_info.format_str(dir_node.attrib['path']))
            print(f"<dir  {tree_info.current_dirpath}/ {dir_path}>")
            assert 'template' not in dir_node.attrib
            working_dir = tree_info.current_dirpath / dir_path
            working_dir.mkdir(parents=True, exist_ok=True)
            dir_tree_info = TemplateTreeInfo(parent=tree_info, current_dirpath=working_dir)
        node_base.NodeBase.treat_action_children_nodes_of(dir_node, execution_context, dir_tree_info)
        return dir_tree_info.current_dirpath
