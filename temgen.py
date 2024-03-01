import xml.etree.ElementTree as XMLTree
from pathlib import Path

from node import template_node
from execution_context import ExecutionContext
from template_tree_info import TemplateTreeInfo
from variables_dict import VariablesDict


class Temgen:
    @staticmethod
    def treat_template_tree_info(execution_context: ExecutionContext,
                                 tree_info: TemplateTreeInfo):
        print('#' * 80)
        print(f"Input file: {tree_info.current_template_filepath}")
        if not tree_info.current_dirpath.exists():
            raise RuntimeError(f"The provided output directory does not exist: '{tree_info.current_dirpath}'.")
        with open(tree_info.current_template_filepath, 'r') as template_file:
            tree = XMLTree.parse(template_file)
            return template_node.TemplateNode.treat_template_node(tree.getroot(), execution_context, tree_info)

    @staticmethod
    def treat_template_file(template_filepath: Path, **kwargs):
        execution_context = kwargs.get("execution_context", None)
        if execution_context is None:
            ui = kwargs["ui"]
            init_variables = kwargs.get("variables", VariablesDict())
            execution_context = ExecutionContext(ui, init_variables)
        else:
            assert "ui" not in kwargs
            assert "variables" not in kwargs
        output_dir = kwargs.get("output_dir", Path.cwd())
        tree_info = TemplateTreeInfo(current_template_filepath=template_filepath,
                                     variables=execution_context.init_variables,
                                     current_dirpath=output_dir)
        Temgen.treat_template_tree_info(execution_context, tree_info)

    @staticmethod
    def find_and_treat_template_file(template_path: Path, version: str | None = None, **kwargs):
        execution_context = kwargs.get("execution_context", None)
        if execution_context is None:
            ui = kwargs["ui"]
            init_variables = kwargs.get("variables", VariablesDict())
            execution_context = ExecutionContext(ui, init_variables)
            kwargs["execution_context"] = execution_context
        template_filepath = execution_context.find_template_file(template_path, version)
        Temgen.treat_template_file(template_filepath, **kwargs)

    @staticmethod
    def treat_template_xml_string(template_str: str, **kwargs):
        execution_context = kwargs.get("execution_context", None)
        if execution_context is None:
            ui = kwargs["ui"]
            init_variables = kwargs.get("variables", VariablesDict())
            execution_context = ExecutionContext(ui, init_variables)
        else:
            assert "ui" not in kwargs
            assert "variables" not in kwargs
        output_dir = kwargs.get("output_dir", Path.cwd())
        tree_info = TemplateTreeInfo(current_template_filepath=None,
                                     variables=execution_context.init_variables,
                                     current_dirpath=output_dir)
        root_element = XMLTree.fromstring(template_str)
        return template_node.TemplateNode.treat_template_node(root_element, execution_context, tree_info)
