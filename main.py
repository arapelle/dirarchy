import xml.etree.ElementTree as XMLTree
from pathlib import Path
import shutil


# https://docs.python.org/3/library/xml.etree.elementtree.html
# https://www.geeksforgeeks.org/how-to-format-a-string-using-a-dictionary-in-python/

# https://regex101.com/r/bJ9aBK/1
# https://regex101.com/delete/YAOjPecUECixMIS0OXvFjDAKs7Cz4PrFN8F6
# https://regex101.com/delete/1/2JyORjGD2XUfgyc9q5pfVBxgQPvUa43XaZOt

class Dirarchy:
    VAR_REGEX = r"[^\{]\{([a-zA-Z0-9_]+)(=(int|float|str))?\}[^\}]"

    def __init__(self):
        self.__variables = dict()

    def treat_dir(self, dir_node: XMLTree.Element, working_dir: Path):
        dir_path = Path(dir_node.attrib['path'])
        print(f"<dir  {working_dir}/ {dir_path}>")
        working_dir /= dir_path
        working_dir.mkdir(parents=True, exist_ok=True)
        for child in dir_node.findall('file'):
            self.treat_file(child, working_dir)
        for child_node in dir_node.findall('dir'):
            self.treat_dir(child_node, working_dir)

    def treat_file(self, file_node: XMLTree.Element, working_dir: Path):
        filepath = file_node.attrib['path']
        print(f"<file {working_dir}/ {filepath}>")
        file_dir = Path(filepath).parent
        (working_dir / file_dir).mkdir(parents=True, exist_ok=True)
        with open(f"{working_dir}/{filepath}", "w") as file:
            file.write(f"{self.file_text(file_node)}")

    def file_text(self, file_node: XMLTree.Element):
        text = file_node.text
        text = text.lstrip()
        if len(text) > 0:
            idx = 1
            while " \t".find(text[-idx]) != -1:
                idx = idx + 1
            text = text[:-idx + 1]
        return text

    def treat_root_dir(self, node: XMLTree.Element):
        output_dpath = Path.cwd() / "output"
        fsys_nodes = node.findall('dir')
        if len(fsys_nodes):
            fsys_node = fsys_nodes[0]
            dir_path = output_dpath / Path(fsys_node.attrib['path'])
            if dir_path.exists():
                shutil.rmtree(dir_path)
            self.treat_dir(fsys_node, output_dpath)
            return
        fsys_nodes = node.findall('file')
        if len(fsys_nodes):
            fsys_node = fsys_nodes[0]
            dir_path = output_dpath / Path(fsys_node.attrib['path'])
            if dir_path.exists():
                shutil.rmtree(dir_path)
            self.treat_dir(fsys_node, output_dpath)


if __name__ == '__main__':
    tree = XMLTree.parse('rsc/dirtree.xml')
    dirarchy = Dirarchy()
    dirarchy.treat_root_dir(tree.getroot())
    vars = dict()
    vars["project_name=str"] = "toto"
    print("{project_name=str}".format_map(vars))
