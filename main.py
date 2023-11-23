import argparse
import xml.etree.ElementTree as XMLTree
from enum import StrEnum, auto
from pathlib import Path
import shutil
import re
import io

from tkinter_ask_dialog import TkinterAskDialog
from terminal_ask_dialog import TerminalAskDialog
import version


class SpecialDict(dict):
    def __missing__(self, key):
        return key.join("{}")


class Dirarchy:
    class UiType(StrEnum):
        TKINTER = auto()
        TERMINAL = auto()

    VAR_NAME_REGEX = re.compile(r'\A[a-zA-Z][a-zA-Z0-9_]*\Z')
    VAR_REGEX = re.compile(r"\{([a-zA-Z][a-zA-Z0-9_]*)\}|(\{\{|\}\})")
    VAR_NAME_GROUP_ID = 1
    SKIP_GROUP_ID = VAR_NAME_GROUP_ID + 1

    def __init__(self, argv=None):
        self.__variables = SpecialDict()
        self._args = self._parse_args(argv)
        match self._args.ui:
            case Dirarchy.UiType.TERMINAL:
                self.__dialog = TerminalAskDialog()
            case Dirarchy.UiType.TKINTER:
                self.__dialog = TkinterAskDialog()
            case _:
                raise Exception(f"Unknown I/O: '{self._args.io}'")

    def _parse_args(self, argv):
        prog_name = 'dirarchy'
        prog_desc = 'A tool generating a directory architecture based on a template.'
        argparser = argparse.ArgumentParser(prog=prog_name, description=prog_desc)
        argparser.add_argument('--version', action='version', version=f'{prog_name} {version.VERSION}')
        argparser.add_argument('-K', f'--{Dirarchy.UiType.TKINTER}'.lower(), action='store_const',
                               dest='ui', const=Dirarchy.UiType.TKINTER, help='Use tkinter I/O.')
        argparser.add_argument('-T', f'--{Dirarchy.UiType.TERMINAL}'.lower(), action='store_const',
                               dest='ui', const=Dirarchy.UiType.TERMINAL, default='terminal', help='Use terminal I/O.')
        argparser.add_argument('-d', '--working-dir', metavar='dir_path',
                               default=Path.cwd(),
                               help='The directory where to generate the directory architecture.')
        argparser.add_argument('dirarchy_xml_file', help='The dirarchy XML file to process.')
        args = argparser.parse_args(argv)
        if args.ui is None:
            args.ui = Dirarchy.UiType.TKINTER
        return args

    def __treat_action_node(self, node: XMLTree.Element, working_dir):
        assert node is not None
        match node.tag:
            case "dir":
                return self.__treat_dir_node(node, working_dir)
            case "file":
                return self.__treat_file_node(node, working_dir)
            case "if":
                return self.__treat_if_node(node, working_dir)
            case _:
                raise Exception(f"Unknown node type: {node.tag}.")

    def __treat_dir_node(self, dir_node: XMLTree.Element, working_dir: Path):
        template_fpath = dir_node.attrib.get('template', None)
        if template_fpath is not None:
            template_fpath = self.__format_str(template_fpath)
            print(f"<dir  {template_fpath}>")
            assert 'path' not in dir_node.attrib
            working_dir = self.treat_xml_file(template_fpath, working_dir, "dir")
        else:
            dir_path = self.__fsys_node_path(dir_node)
            print(f"<dir  {working_dir}/ {dir_path}>")
            assert 'template' not in dir_node.attrib
            working_dir /= dir_path
            working_dir.mkdir(parents=True, exist_ok=True)
        for child_node in dir_node:
            self.__treat_action_node(child_node, working_dir)
        return working_dir

    def __treat_file_node(self, file_node: XMLTree.Element, working_dir: Path):
        template_fpath = file_node.attrib.get('template', None)
        if template_fpath is not None:
            template_fpath = self.__format_str(template_fpath)
            print(f"<dir  {template_fpath}>")
            assert 'path' not in file_node.attrib
            working_dir = self.treat_xml_file(template_fpath, working_dir, "file")
        else:
            filepath = self.__fsys_node_path(file_node)
            print(f"<file {working_dir}/ {filepath}>")
            assert 'template' not in file_node.attrib
            file_dir = Path(filepath).parent
            working_dir /= file_dir
            working_dir.mkdir(parents=True, exist_ok=True)
            with open(f"{working_dir}/{filepath.name}", "w") as file:
                file.write(f"{self.__file_text(file_node)}")
        return working_dir

    def __file_text(self, file_node: XMLTree.Element):
        text: str = self.__strip_text(file_node.text)
        content_attr = file_node.attrib.get('content')
        if content_attr is None:
            content_attr = "format"
        content_attr_list: list = content_attr.split('|')
        if not content_attr_list or "raw" in content_attr_list:
            return text
        if "format" in content_attr_list:
            text = self.__super_format_str(text)
        elif "super_format" in content_attr_list:
            text = self.__super_format_str(text)
        return text

    def __treat_if_node(self, if_node: XMLTree.Element, working_dir: Path):
        expr_attr = if_node.attrib['expr']
        expr_attr = self.__format_str(expr_attr)
        b_expr = eval(expr_attr)
        if b_expr:
            for child_node in if_node:
                self.__treat_action_node(child_node, working_dir)
        return working_dir

    def __format_str(self, text: str):
        neo_text: str = ""
        for line in io.StringIO(text):
            neo_text += line.format_map(self.__variables)
        return neo_text

    def __super_format_str(self, text: str):
        neo_text: str = ""
        for line in io.StringIO(text):
            index = 0
            neo_line = ""
            for mre in re.finditer(self.VAR_REGEX, line):
                if mre.group(self.SKIP_GROUP_ID):
                    neo_line += line[index:mre.start(self.SKIP_GROUP_ID)] + mre.group(self.SKIP_GROUP_ID)[0]
                    index = mre.end(self.SKIP_GROUP_ID)
                    continue
                var_name = mre.group(self.VAR_NAME_GROUP_ID)
                neo_line += line[index:mre.start(0)]
                index = mre.end(0)
                if var_name not in self.__variables:
                    raise Exception(f"Variable not set: '{var_name}'!")
                neo_line += self.__variables[var_name]
                # print(f"Var: {var_name} = '{self.__variables[var_name]}'")
            neo_line += line[index:]
            neo_text += neo_line
        return neo_text

    def __strip_text(self, text):
        text = text.lstrip()
        if len(text) > 0:
            idx = 1
            while " \t".find(text[-idx]) != -1:
                idx = idx + 1
            text = text[:-idx + 1]
        return text

    def __fsys_node_path(self, dir_node):
        dir_path_str = dir_node.attrib['path']
        dir_path_str = self.__format_str(dir_path_str)
        dir_path = Path(dir_path_str)
        return dir_path

    def treat_root_node(self, dirarchy_node: XMLTree.Element, working_dir, expect):
        self.__treat_vars_node(dirarchy_node.find("vars"))
        dir_nodes = dirarchy_node.findall("dir")
        fsys_node = dir_nodes[0] if len(dir_nodes) > 0 else None
        if fsys_node is None:
            if expect == "dir":
                raise Exception("Directory template was expected!")
            file_nodes = dirarchy_node.findall("file")
            fsys_node = file_nodes[0] if len(file_nodes) > 0 else None
            if expect == "file":
                raise Exception("File template was expected!")
        return self.__treat_action_node(fsys_node, working_dir)

    def __treat_vars_node(self, vars_node: XMLTree.Element):
        if vars_node is None:
            return
        for var_node in vars_node.iterfind("var"):
            self.__treat_var_node(var_node)

    def __treat_var_node(self, var_node: XMLTree.Element):
        var_name = var_node.attrib.get('name')
        if not re.match(self.VAR_NAME_REGEX, var_name):
            raise Exception(f"Variable name is not a valid name: '{var_name}'.")
        if var_name not in self.__variables:
            var_value = var_node.attrib.get('value', None)
            if var_value is not None:
                var_value = self.__format_str(var_value)
            else:
                var_type = var_node.attrib.get('type', 'str')
                var_default = var_node.attrib.get('default', None)
                var_value = self.__dialog.ask_valid_var(var_type, var_name, var_default)
            self.__variables[var_name] = var_value
            # print(f"{var_name}:{var_type}({var_default})={var_value}")

    def treat_xml_file(self, dirarchy_fpath, working_dir, expect):
        assert expect is None or expect == "dir" or expect == "file"
        print('#' * 80)
        print(f"Input file: {dirarchy_fpath}")
        with open(dirarchy_fpath, 'r') as dirarchy_file:
            tree = XMLTree.parse(dirarchy_file)
            return self.treat_root_node(tree.getroot(), working_dir, expect)

    def treat_root_xml_file(self, dirarchy_fpath, working_dir=Path.cwd()):
        self.treat_xml_file(dirarchy_fpath, working_dir, None)


if __name__ == '__main__':
    output_dpath = Path.cwd() / "output"
    if output_dpath.exists():
        shutil.rmtree(output_dpath)
    output_dpath.mkdir(parents=True)
    dirarchy = Dirarchy()
    # dirarchy.treat_root_xml_file('rsc/dirtree.xml', output_dpath)
    # dirarchy.treat_root_xml_file('rsc/fdirtree.xml', output_dpath)
    dirarchy.treat_root_xml_file('rsc/rscdirtree.xml', output_dpath)
