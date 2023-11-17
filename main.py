import tkinter
import xml.etree.ElementTree as XMLTree
from builtins import isinstance
from pathlib import Path
import shutil
import re
import io
from tkinter import simpledialog, messagebox


def cancel_generation(res=0):
    print("CANCEL!")
    exit(res)


def ask_str_value(label: str, default: str):
    return simpledialog.askstring(label, label + ": ", initialvalue=default)


def ask_bool_value(label: str):
    return messagebox.askyesnocancel(label, label)


def ask_valid_value(label: str, default, check_fn=lambda value: len(value) > 0):
    value_is_bool = isinstance(default, type(True))
    value = None if value_is_bool else ""
    while not check_fn(value):
        if value_is_bool:
            value = ask_bool_value(label)
        else:
            value = ask_str_value(label, default)
        if value is None:
            cancel_generation()
        print(f"Parameter '{label}': '{value}'")
    return value


def ask_valid_bool_value(label: str):
    return ask_valid_value(label, True,
                           lambda value: value is not None and isinstance(value, type(True)))


def ask_valid_int_value(label: str, default="0"):
    return ask_valid_value(label, default,
                           lambda value: bool(re.match(r"\A-?\d+\Z", value.strip())))


def ask_valid_uint_value(label: str, default="0"):
    return ask_valid_value(label, default,
                           lambda value: bool(re.match(r"\A\d+\Z", value.strip())))


def ask_valid_float_value(label: str, default="0.0"):
    return ask_valid_value(label, default,
                           lambda value: bool(re.match(r"\A-?\d+(\.\d+)?\Z", value.strip())))


def ask_valid_var(parameter_type: str, label: str, default=""):
    match parameter_type:
        case 'int':
            return ask_valid_int_value(label, default)
        case 'uint':
            return ask_valid_int_value(label, default)
        case 'float':
            return ask_valid_int_value(label, default)
        case 'str':
            return ask_valid_value(label, default)
        case _:
            raise f"Bad parameter_type: '{parameter_type}'"


class SpecialDict(dict):
    def __missing__(self, key):
        return key.join("{}")


class Dirarchy:
    VAR_REGEX = re.compile(r"\{([a-zA-Z][a-zA-Z0-9_]*)(\[(int|uint|float|str)\])?(='(([^']|\\')*)')?\}"
                           r"|(\{\{|\}\})")
    VAR_NAME_GROUP_ID = 1
    VAR_TYPE_GROUP_ID = VAR_NAME_GROUP_ID + 2
    VAR_DEFAULT_VALUE_GROUP_ID = VAR_TYPE_GROUP_ID + 2
    SKIP_GROUP_ID = VAR_DEFAULT_VALUE_GROUP_ID + 2

    def __init__(self):
        self.__variables = SpecialDict()
        self.__variables['namespace'] = 'arba'
        self.__variables['base_name'] = 'core'
        self.__variables['subdir'] = 'feature'
        # self.__variables['version'] = '1'

    def __treat_dir_node(self, dir_node: XMLTree.Element, working_dir: Path):
        dir_path = self.__fsys_node_path(dir_node)
        print(f"<dir  {working_dir}/ {dir_path}>")
        working_dir /= dir_path
        working_dir.mkdir(parents=True, exist_ok=True)
        for child in dir_node.findall('file'):
            self.__treat_file_node(child, working_dir)
        for child_node in dir_node.findall('dir'):
            self.__treat_dir_node(child_node, working_dir)

    def __treat_file_node(self, file_node: XMLTree.Element, working_dir: Path):
        filepath = self.__fsys_node_path(file_node)
        print(f"<file {working_dir}/ {filepath}>")
        file_dir = Path(filepath).parent
        (working_dir / file_dir).mkdir(parents=True, exist_ok=True)
        with open(f"{working_dir}/{filepath}", "w") as file:
            file.write(f"{self.__file_text(file_node)}")

    def __file_text(self, file_node: XMLTree.Element):
        text: str = self.__strip_text(file_node.text)
        content_attr = file_node.attrib.get('content')
        if content_attr is None:
            content_attr = "format"
        content_attr_list: list = content_attr.split('|')
        if not content_attr_list or "raw" in content_attr_list:
            return text
        if "format" in content_attr_list:
            text = self.__format_str(text)
        return text

    def __format_str(self, text: str):
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
                var_type = mre.group(self.VAR_TYPE_GROUP_ID)
                var_type = "str" if var_type is None else var_type
                var_default_value = mre.group(self.VAR_DEFAULT_VALUE_GROUP_ID)
                neo_line += line[index:mre.start(0)]
                index = mre.end(0)
                var_value = var_default_value
                if var_name not in self.__variables:
                    var_value = ask_valid_var(var_type, var_name, var_value)
                    self.__variables[var_name] = var_value
                else:
                    var_value = self.__variables[var_name]
                neo_line += var_value
                # print(f"Var: {var_name}: {var_type} = '{self.__variables[var_name]}'")
            neo_line += line[index:]
            neo_text += neo_line
        return neo_text  # text.format_map(self.__variables)

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

    def treat_root_node(self, node: XMLTree.Element):
        output_dpath = Path.cwd() / "output"
        self.__treat_vars_node(node.find("vars"))
        dir_nodes = node.findall("dir")
        fsys_node = dir_nodes[0] if len(dir_nodes) > 0 else None
        if fsys_node is None:
            file_nodes = node.findall("file")
            fsys_node = file_nodes[0] if len(file_nodes) > 0 else None
        assert fsys_node is not None
        fsys_node_path = output_dpath / self.__fsys_node_path(fsys_node)
        if fsys_node_path.exists():
            print(f"rm {fsys_node_path}")
            shutil.rmtree(fsys_node_path)
        if fsys_node.tag == "dir":
            self.__treat_dir_node(fsys_node, output_dpath)
        elif fsys_node.tag == "file":
            self.__treat_file_node(fsys_node, output_dpath)
        else:
            assert False  # Unknown first node type

    def __treat_vars_node(self, vars_node: XMLTree.Element):
        if vars_node is None:
            return
        for var_node in vars_node.iterfind("var"):
            self.__treat_var_node(var_node)

    def __treat_var_node(self, var_node: XMLTree.Element):
        var_name = var_node.attrib.get('name')
        var_type = var_node.attrib.get('type', 'str')
        var_default = var_node.attrib.get('default', '')
        var_value = ask_valid_var(var_type, var_name, var_default)
        self.__variables[var_name] = var_value
        # print(f"{var_name}:{var_type}({var_default})={var_value}")

    def treat_xml_file(self, dirarchy_fpath):
        print('#' * 80)
        print(f"Input file: {dirarchy_fpath}")
        with open(dirarchy_fpath, 'r') as dirarchy_file:
            tree = XMLTree.parse(dirarchy_file)
            self.treat_root_node(tree.getroot())


if __name__ == '__main__':
    gui = tkinter.Tk()
    gui.withdraw()
    dirarchy = Dirarchy()
    # dirarchy.treat_xml_file('rsc/dirtree.xml')
    dirarchy.treat_xml_file('rsc/fdirtree.xml')
