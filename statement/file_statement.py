import xml.etree.ElementTree as XMLTree
from pathlib import Path

from log import MethodScopeLog
from statement.abstract_main_statement import AbstractMainStatement


class FileStatement(AbstractMainStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractMainStatement, **kargs):
        super().__init__(current_node, parent_statement, **kargs)
        self.__output_filepath = Path()
        self.__output_file = None

    def __del__(self):
        if self.__output_file is not None:
            self.__output_file.close()

    def current_file_statement(self):
        return self

    def current_output_filepath(self):
        return self.__output_filepath

    def current_output_file(self):
        return self.__output_file

    def extract_current_output_file(self):
        output_file = self.__output_file
        self.__output_file = None
        return output_file

    def run(self):
        with MethodScopeLog(self):
            template_path = self.current_node().get('template', None)
            if template_path is None:
                self.__make_output_file()
            else:
                self.__run_template(template_path)
            self.treat_children_nodes_of(self.current_node())

    def __make_output_file(self):
        parent_output_dirpath = self.parent_statement().current_dir_statement().current_output_dirpath()
        self.__output_filepath = Path(parent_output_dirpath / self.format_str(self.current_node().attrib['path']))
        output_file_parent_dirpath = self.__output_filepath.parent
        if output_file_parent_dirpath != parent_output_dirpath:
            self.logger.info(f"Make dir {output_file_parent_dirpath}")
            output_file_parent_dirpath.mkdir(parents=True, exist_ok=True)
        open_mode = "w"
        self.logger.info(f"Make file {self.__output_filepath}")
        self.__output_file = open(self.__output_filepath, open_mode)
        self.__output_file.write(self.__file_text(self.current_node()))
        self.__output_file.flush()

    def __run_template(self, template_path: str):
        assert 'path' not in self.current_node().attrib
        template_path = Path(self.format_str(template_path))
        version_attr = self.current_node().get('template-version', None)
        if version_attr:
            version_attr = self.format_str(version_attr)
        template_path = self.temgen().find_template_file(template_path, version_attr)
        from statement.template_statement import TemplateStatement
        with open(template_path, 'r') as template_file:
            data_tree = XMLTree.parse(template_file)
        template_statement = TemplateStatement(data_tree.getroot(), self,
                                               variables=self.variables(),
                                               template_filepath=template_path)
        template_statement.run()
        expected_statement = template_statement.expected_statement()
        assert isinstance(expected_statement, self.__class__)
        self.__output_filepath = expected_statement.current_output_filepath()
        self.__output_file = expected_statement.extract_current_output_file()

    def treat_child_node(self, node: XMLTree.Element, child_node: XMLTree.Element):
        super().treat_child_node(node, child_node)
        # TODO match: <contents>

    def __file_text(self, file_node: XMLTree.Element):
        copy_attr = file_node.attrib.get('copy')
        if copy_attr is None:
            text: str = "" if file_node.text is None else FileStatement.strip_text(file_node.text)
        else:
            copy_attr = self.format_str(copy_attr)
            with open(copy_attr) as copied_file:
                text: str = copied_file.read()
        format_attr = file_node.attrib.get('format', "format")
        format_attr_list: list = [self.format_str(fstr) for fstr in format_attr.split('|')]
        if len(format_attr_list) == 0 or "format" in format_attr_list:
            text = self.format_str(text)
        elif "raw" in format_attr_list:
            pass
        return text

    @staticmethod
    def strip_text(text: str):
        text = text.lstrip()
        if len(text) > 0:
            idx = 0
            while " \t".find(text[-(idx + 1)]) != -1:
                idx = idx + 1
            if idx > 0:
                text = text[:-idx]
        return text
