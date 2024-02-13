import xml.etree.ElementTree as XMLTree
from pathlib import Path

import temgen_node
from ask_dialog import AskDialog
from execution_context import ExecutionContext
from template_tree_info import TemplateTreeInfo
from variables_dict import VariablesDict


class Temgen:
    @staticmethod
    def treat_tree_current_temgen_file(execution_context: ExecutionContext,
                                       tree_info: TemplateTreeInfo):
        print('#' * 80)
        print(f"Input file: {tree_info.current_temgen_filepath}")
        with open(tree_info.current_temgen_filepath, 'r') as temgen_file:
            tree = XMLTree.parse(temgen_file)
            return temgen_node.TemgenNode.treat_temgen_node(tree.getroot(), execution_context, tree_info)

    @staticmethod
    def treat_temgen_file(temgen_filepath: Path, ui: AskDialog,
                          init_variables: None | VariablesDict = None,
                          output_dir: Path = Path.cwd()):
        if init_variables is None:
            init_variables = VariablesDict()
        execution_context = ExecutionContext(ui, init_variables)
        tree_info = TemplateTreeInfo(current_temgen_filepath=temgen_filepath,
                                     current_dirpath=output_dir)
        Temgen.treat_tree_current_temgen_file(execution_context, tree_info)
