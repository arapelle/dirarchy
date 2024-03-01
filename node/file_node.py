import xml.etree.ElementTree as XMLTree
from pathlib import Path

import temgen
from execution_context import ExecutionContext
from template_tree_info import TemplateTreeInfo


class FileNode:
    @staticmethod
    def treat_file_node(file_node: XMLTree.Element,
                        execution_context: ExecutionContext,
                        tree_info: TemplateTreeInfo):
        template_path = file_node.attrib.get('template', None)
        if template_path is not None:
            print(f"<file  {template_path}>")
            assert 'path' not in file_node.attrib
            template_path = Path(tree_info.format_str(template_path))
            version_attr = file_node.attrib.get('template-version', None)
            if version_attr:
                version_attr = tree_info.format_str(version_attr)
            template_path = execution_context.find_template_file(template_path, version_attr)
            template_tree_info = TemplateTreeInfo(parent=tree_info,
                                                  expected_root_node_type=TemplateTreeInfo.RootNodeType.FILE,
                                                  current_template_filepath=Path(template_path))
            working_dir = temgen.Temgen.treat_template_tree_info(execution_context, template_tree_info)
            file_tree_info = TemplateTreeInfo(parent=tree_info, current_dirpath=working_dir)
            file_tree_info.variables = template_tree_info.variables
        else:
            filepath = Path(tree_info.format_str(file_node.attrib['path']))
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
                file.write(f"{FileNode.file_text(file_node, file_tree_info)}")
        return file_tree_info.current_dirpath

    @staticmethod
    def file_text(file_node: XMLTree.Element, tree_info: TemplateTreeInfo):
        copy_attr = file_node.attrib.get('copy')
        if copy_attr is None:
            text: str = "" if file_node.text is None else FileNode.strip_text(file_node.text)
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

    @staticmethod
    def strip_text(text):
        text = text.lstrip()
        if len(text) > 0:
            idx = 0
            while " \t".find(text[-(idx + 1)]) != -1:
                idx = idx + 1
            if idx > 0:
                text = text[:-idx + 1]
        return text
