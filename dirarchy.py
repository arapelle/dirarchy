import xml.etree.ElementTree as XMLTree

import dirarchy_node
from execution_context import ExecutionContext
from template_tree_info import TemplateTreeInfo


class Dirarchy:
    @staticmethod
    def treat_xml_file(execution_context: ExecutionContext,
                       tree_info: TemplateTreeInfo):
        print('#' * 80)
        print(f"Input file: {tree_info.current_temgen_filepath}")
        with open(tree_info.current_temgen_filepath, 'r') as dirarchy_file:
            tree = XMLTree.parse(dirarchy_file)
            return dirarchy_node.DirarchyNode.treat_dirarchy_node(tree.getroot(), execution_context, tree_info)
