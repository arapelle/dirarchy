import argparse
import xml.etree.ElementTree as XMLTree
from enum import StrEnum, auto
from pathlib import Path
import re

import constants
import random_var_value
import regex
from execution_context import ExecutionContext
from template_tree_info import TemplateTreeInfo
from tkinter_ask_dialog import TkinterAskDialog
from terminal_ask_dialog import TerminalAskDialog
import version
from variables_dict import VariablesDict


class RegexFullMatch:
    def __init__(self, regex_pattern):
        if isinstance(regex_pattern, re.Pattern):
            self.__regex = regex_pattern
        else:
            self.__regex = re.compile(regex_pattern)

    def __call__(self, value_to_check: str):
        return re.fullmatch(self.__regex, value_to_check)


class Dirarchy:
    class UiType(StrEnum):
        TKINTER = auto()
        TERMINAL = auto()

    def __init__(self, argv=None):
        self._args = self._parse_args(argv)
        self.__set_execution_context_from_args()

    @property
    def args(self):
        return self._args

    def run(self):
        if self.args.output_dir.exists():
            self.treat_xml_file(self.args.dirarchy_xml_file, self.__execution_context, self.args.output_dir)
        else:
            raise Exception(f"The provided output directory does not exist: '{self.args.output_dir}'.")

    def __set_execution_context_from_args(self):
        match self.args.ui:
            case Dirarchy.UiType.TERMINAL:
                ui = TerminalAskDialog()
            case Dirarchy.UiType.TKINTER:
                ui = TkinterAskDialog()
            case _:
                raise Exception(f"Unknown I/O: '{self.args.io}'")
        variables = VariablesDict()
        if self.args.var:
            variables.update_vars_from_dict(self.args.var)
        if self.args.var_file:
            variables.update_vars_from_files(self.args.var_file)
        if self.args.custom_ui:
            variables.update_vars_from_custom_ui(self.args.custom_ui)
        self.__execution_context = ExecutionContext(ui, variables)

    def _parse_args(self, argv=None):
        prog_name = 'dirarchy'
        prog_desc = 'A tool generating a directory architecture based on a template.'
        argparser = argparse.ArgumentParser(prog=prog_name, description=prog_desc)
        argparser.add_argument('--version', action='version', version=f'{prog_name} {version.VERSION}')
        argparser.add_argument('-K', f'--{Dirarchy.UiType.TKINTER}'.lower(), action='store_const',
                               dest='ui', const=Dirarchy.UiType.TKINTER, help='Use tkinter I/O.')
        argparser.add_argument('-T', f'--{Dirarchy.UiType.TERMINAL}'.lower(), action='store_const',
                               dest='ui', const=Dirarchy.UiType.TERMINAL, default='terminal', help='Use terminal I/O.')
        argparser.add_argument('-C', '--custom-ui', metavar='custom_ui_cmd',
                               help='Use a custom user interface to set variables before treating them with dirarchy. '
                                    '(Executing custom_ui_cmd in shell is expected to use the desired custom '
                                    'interface.)')
        argparser.add_argument('-o', '--output-dir', metavar='dir_path',
                               default=Path.cwd(),
                               help='The directory where to generate the desired hierarchy (dir or file).')
        argparser.add_argument('-v', '--var', metavar='key=value', nargs='+',
                               type=Dirarchy.__var_from_key_value_str,
                               help='Set variables.')
        argparser.add_argument('--var-file', metavar='var_json_files', nargs='+',
                               help='Set variables from a JSON files.')
        argparser.add_argument('dirarchy_xml_file',
                               help='The dirarchy XML file to process.')
        args = argparser.parse_args(argv)
        if args.ui is None:
            args.ui = Dirarchy.UiType.TKINTER
        args.output_dir = Path(args.output_dir)
        return args

    @classmethod
    def __var_from_key_value_str(cls, key_value_str: str):
        key, value = key_value_str.split('=')
        if re.match(regex.VAR_NAME_REGEX, key):
            return key, value
        raise RuntimeError(key_value_str)

    def __treat_action_node(self, node: XMLTree.Element, execution_context: ExecutionContext,
                            tree_info: TemplateTreeInfo):
        assert node is not None
        match node.tag:
            case "dir":
                self.__treat_dir_node(node, execution_context, tree_info)
            case "file":
                self.__treat_file_node(node, execution_context, tree_info)
            case "if":
                self.__treat_if_node(node, execution_context, tree_info)
            case "match":
                self.__treat_match_node(node, execution_context, tree_info)
            case _:
                raise Exception(f"Unknown node type: {node.tag}.")

    def __treat_dir_node(self, dir_node: XMLTree.Element, execution_context: ExecutionContext,
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
            working_dir = self.__treat_xml_file(execution_context, template_tree_info)
            dir_tree_info = TemplateTreeInfo(parent=tree_info, current_dirpath=working_dir)
            dir_tree_info.variables = template_tree_info.variables
        else:
            dir_path = self.__fsys_node_path(dir_node, tree_info)
            print(f"<dir  {tree_info.current_dirpath}/ {dir_path}>")
            assert 'template' not in dir_node.attrib
            working_dir = tree_info.current_dirpath / dir_path
            working_dir.mkdir(parents=True, exist_ok=True)
            dir_tree_info = TemplateTreeInfo(parent=tree_info, current_dirpath=working_dir)
        self.__treat_action_children_nodes_of(dir_node, execution_context, dir_tree_info)
        return dir_tree_info.current_dirpath

    def __treat_file_node(self, file_node: XMLTree.Element, execution_context: ExecutionContext,
                          tree_info: TemplateTreeInfo):
        template_fpath = file_node.attrib.get('template', None)
        if template_fpath is not None:
            print(f"<file  {template_fpath}>")
            assert 'path' not in file_node.attrib
            template_fpath = Path(tree_info.format_str(template_fpath))
            version_attr = file_node.attrib.get('template-version', None)
            if version_attr:
                version_attr = tree_info.format_str(version_attr)
            template_fpath = execution_context.find_template(template_fpath, version_attr)
            template_tree_info = TemplateTreeInfo(parent=tree_info,
                                                  expected_root_node_type=TemplateTreeInfo.RootNodeType.FILE,
                                                  current_temgen_filepath=Path(template_fpath))
            working_dir = self.__treat_xml_file(execution_context, template_tree_info)
            file_tree_info = TemplateTreeInfo(parent=tree_info, current_dirpath=working_dir)
            file_tree_info.variables = template_tree_info.variables
        else:
            filepath = self.__fsys_node_path(file_node, tree_info)
            print(f"<file {tree_info.current_dirpath}/ {filepath}>")
            assert 'template' not in file_node.attrib
            current_filepath = tree_info.current_dirpath / filepath
            current_dirpath = current_filepath.parent
            current_dirpath.mkdir(parents=True, exist_ok=True)
            with open(current_filepath, "w") as file:
                file_tree_info = TemplateTreeInfo(parent=tree_info,
                                                  current_dirpath=current_dirpath,
                                                  current_filepath=current_filepath,
                                                  current_file=file)
                file.write(f"{self.__file_text(file_node, file_tree_info)}")
        return file_tree_info.current_dirpath

    def __file_text(self, file_node: XMLTree.Element, tree_info: TemplateTreeInfo):
        copy_attr = file_node.attrib.get('copy')
        if copy_attr is None:
            text: str = "" if file_node.text is None else self.__strip_text(file_node.text)
        else:
            copy_attr = tree_info.format_str(copy_attr)
            with open(copy_attr) as copied_file:
                text: str = copied_file.read()
        format_attr = file_node.attrib.get('format', "format")
        format_attr_list: list = [tree_info.format_str(fstr) for fstr in format_attr.split('|')]
        if len(format_attr_list) == 0 or "format" in format_attr_list:
            text = tree_info.format_str(text)
        elif "super_format" in format_attr_list:
            text = tree_info.super_format_str(text)
        elif "raw" in format_attr_list:
            pass
        return text

    def __treat_if_node(self, if_node: XMLTree.Element, execution_context: ExecutionContext,
                        tree_info: TemplateTreeInfo):
        from re import match, fullmatch
        then_nodes = if_node.findall('then')
        else_nodes = if_node.findall('else')
        then_count = len(then_nodes)
        else_count = len(else_nodes)
        if then_count > 1:
            raise Exception("Too many 'then' nodes for a 'if' node.")
        if else_count > 1:
            raise Exception("Too many 'else' nodes for a 'if' node.")
        if else_count and then_count == 0:
            raise Exception("A 'else' node is provided for a 'if' node but a 'then' node is missing.")
        expr_attr = if_node.attrib['expr']
        expr_attr = tree_info.format_str(expr_attr)
        b_expr = eval(expr_attr)
        if b_expr:
            if then_count == 0:
                self.__treat_action_children_nodes_of(if_node, execution_context, tree_info)
            else:
                self.__treat_action_children_nodes_of(then_nodes[0], execution_context, tree_info)
        elif else_count > 0:
            self.__treat_action_children_nodes_of(else_nodes[0], execution_context, tree_info)

    def __treat_action_children_nodes_of(self, node, execution_context: ExecutionContext, tree_info: TemplateTreeInfo):
        for child_node in node:
            self.__treat_action_node(child_node, execution_context, tree_info)

    def __treat_match_node(self, match_node: XMLTree.Element, execution_context: ExecutionContext,
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
            self.__treat_action_children_nodes_of(found_case_node, execution_context, tree_info)
        elif default_case_node:
            self.__treat_action_children_nodes_of(default_case_node, execution_context, tree_info)

    def __strip_text(self, text):
        text = text.lstrip()
        if len(text) > 0:
            idx = 0
            while " \t".find(text[-(idx + 1)]) != -1:
                idx = idx + 1
            if idx > 0:
                text = text[:-idx + 1]
        return text

    def __fsys_node_path(self, fsys_node, tree_info: TemplateTreeInfo):
        dir_path_str = fsys_node.attrib['path']
        dir_path_str = tree_info.format_str(dir_path_str)
        dir_path = Path(dir_path_str)
        return dir_path

    def __treat_root_node(self, dirarchy_node: XMLTree.Element, execution_context: ExecutionContext,
                          tree_info: TemplateTreeInfo):
        if dirarchy_node.tag != constants.ROOT_NODE_NAME:
            raise RuntimeError(f"Root node must be '{constants.ROOT_NODE_NAME}'!")
        self.__treat_vars_node(dirarchy_node.find("vars"), execution_context, tree_info)
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
                return self.__treat_dir_node(fsys_node, execution_context, tree_info)
            case "file":
                return self.__treat_file_node(fsys_node, execution_context, tree_info)
            case _:
                assert False

    def __treat_vars_node(self, vars_node: XMLTree.Element, execution_context: ExecutionContext,
                          tree_info: TemplateTreeInfo):
        if vars_node is None:
            return
        for var_node in vars_node.iterfind("var"):
            self.__treat_var_node(var_node, execution_context, tree_info)

    def __treat_var_node(self, var_node: XMLTree.Element, execution_context: ExecutionContext,
                         tree_info: TemplateTreeInfo):
        var_name = var_node.attrib.get('name')
        if not re.match(regex.VAR_NAME_REGEX, var_name):
            raise Exception(f"Variable name is not a valid name: '{var_name}'.")
        if var_name not in tree_info.variables:
            var_value = var_node.attrib.get('value', None)
            if var_value is not None:
                var_value = tree_info.format_str(var_value)
            else:
                var_rand_value = var_node.attrib.get('rand_value', None)
                if var_rand_value is not None:
                    var_value = random_var_value.random_var_value(var_rand_value)
                else:
                    var_type = var_node.attrib.get('type', 'str')
                    var_default = var_node.attrib.get('default', None)
                    var_restr = var_node.attrib.get('regex', None)
                    regex_full_match = RegexFullMatch(var_restr) if var_restr is not None else None
                    var_value = execution_context.ui.ask_valid_var(var_type, var_name, var_default, regex_full_match)
            tree_info.variables[var_name] = var_value
            # print(f"{var_name}:{var_type}({var_default})={var_value}")

    def __treat_xml_file(self, execution_context: ExecutionContext, tree_info: TemplateTreeInfo):
        print('#' * 80)
        print(f"Input file: {tree_info.current_temgen_filepath}")
        with open(tree_info.current_temgen_filepath, 'r') as dirarchy_file:
            tree = XMLTree.parse(dirarchy_file)
            return self.__treat_root_node(tree.getroot(), execution_context, tree_info)

    def treat_xml_file(self, dirarchy_fpath, execution_context: ExecutionContext, working_dir=Path.cwd()):
        tree_info = TemplateTreeInfo(current_temgen_filepath=Path(dirarchy_fpath),
                                     current_dirpath=working_dir)
        tree_info.variables = execution_context.init_variables
        self.__treat_xml_file(execution_context, tree_info)


if __name__ == '__main__':
    dirarchy = Dirarchy()
    dirarchy.run()
