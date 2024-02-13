import xml.etree.ElementTree as XMLTree
from pathlib import Path

import temgen
from execution_context import ExecutionContext
import node_base
from template_tree_info import TemplateTreeInfo


class DirNode:
    @staticmethod
    def treat_dir_node(dir_node: XMLTree.Element,
                       execution_context: ExecutionContext,
                       tree_info: TemplateTreeInfo):
        template_fpath = dir_node.attrib.get('template', None)
        if template_fpath is not None:
            print(f"<dir  {template_fpath}>")
            assert 'path' not in dir_node.attrib
            template_fpath = Path(tree_info.format_str(template_fpath))
            version_attr = dir_node.attrib.get('template-version', None)
            if version_attr:
                version_attr = tree_info.format_str(version_attr)
            template_fpath = execution_context.find_template(template_fpath, version_attr)
            template_tree_info = TemplateTreeInfo(parent=tree_info,
                                                  expected_root_node_type=TemplateTreeInfo.RootNodeType.DIRECTORY,
                                                  current_temgen_filepath=Path(template_fpath))
            working_dir = temgen.Temgen.treat_tree_current_temgen_file(execution_context, template_tree_info)
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
