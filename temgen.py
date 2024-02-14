import xml.etree.ElementTree as XMLTree
from pathlib import Path

import temgen_node
from execution_context import ExecutionContext
from template_tree_info import TemplateTreeInfo
from variables_dict import VariablesDict


class Temgen:
    @staticmethod
    def treat_tree_current_temgen_file(execution_context: ExecutionContext,
                                       tree_info: TemplateTreeInfo):
        print('#' * 80)
        print(f"Input file: {tree_info.current_temgen_filepath}")
        if not tree_info.current_dirpath.exists():
            raise RuntimeError(f"The provided output directory does not exist: '{tree_info.current_dirpath}'.")
        with open(tree_info.current_temgen_filepath, 'r') as temgen_file:
            tree = XMLTree.parse(temgen_file)
            return temgen_node.TemgenNode.treat_temgen_node(tree.getroot(), execution_context, tree_info)

    @staticmethod
    def treat_temgen_file(temgen_filepath: Path, **kwargs):
        execution_context = kwargs.get("execution_context", None)
        if execution_context is None:
            ui = kwargs["ui"]
            init_variables = kwargs.get("variables", VariablesDict())
            execution_context = ExecutionContext(ui, init_variables)
        else:
            assert "ui" not in kwargs
            assert "variables" not in kwargs
        output_dir = kwargs.get("output_dir", Path.cwd())
        tree_info = TemplateTreeInfo(current_temgen_filepath=temgen_filepath,
                                     variables=execution_context.init_variables,
                                     current_dirpath=output_dir)
        Temgen.treat_tree_current_temgen_file(execution_context, tree_info)

    @staticmethod
    def treat_temgen_template(temgen_path: Path, version: str | None = None, **kwargs):
        execution_context = kwargs.get("execution_context", None)
        if execution_context is None:
            ui = kwargs["ui"]
            init_variables = kwargs.get("variables", VariablesDict())
            execution_context = ExecutionContext(ui, init_variables)
        else:
            assert "ui" not in kwargs
            assert "variables" not in kwargs
        temgen_filepath = execution_context.find_temgen_file(temgen_path, version)
        output_dir = kwargs.get("output_dir", Path.cwd())
        tree_info = TemplateTreeInfo(current_temgen_filepath=temgen_filepath,
                                     variables=execution_context.init_variables,
                                     current_dirpath=output_dir)
        Temgen.treat_tree_current_temgen_file(execution_context, tree_info)
