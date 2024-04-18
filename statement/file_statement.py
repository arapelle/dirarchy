import xml.etree.ElementTree as XMLTree
from pathlib import Path

from statement.abstract_contents_statement import AbstractContentsStatement
from statement.abstract_main_statement import AbstractMainStatement


class FileStatement(AbstractContentsStatement):
    from statement.template_statement import TemplateStatement

    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractMainStatement, **kargs):
        super().__init__(current_node, parent_statement, **kargs)
        self.__output_filepath = Path()

    def __del__(self):
        if self._output_stream is not None:
            self._output_stream.close()
            self._output_stream = None

    def current_file_statement(self):
        return self

    def current_output_filepath(self):
        return self.__output_filepath

    def current_output_file(self):
        return self._output_stream

    def allows_template(self):
        return True

    def execute(self):
        self.__make_output_file()

    def __make_output_file(self):
        self.__resolve_output_filepath_and_ensure_output_dir()
        self.logger.info(f"Make file: {self.__output_filepath}")
        self.__open_output_file()
        copy_attr = self.current_node().attrib.get("copy", None)
        if copy_attr is not None:
            self._copy_file_to_output(copy_attr, self)
        else:
            if "copy-encoding" in self.current_node().attrib:
                raise RuntimeError("'copy-encoding is provided but copy is missing.")
        self.treat_children_nodes()
        self._output_stream.flush()

    def __resolve_output_filepath_and_ensure_output_dir(self):
        parent_output_dirpath = self.parent_statement().current_dir_statement().current_output_dirpath()
        self.__output_filepath = Path(parent_output_dirpath / self.format_str(self.current_node().attrib['path']))
        output_file_parent_dirpath = self.__output_filepath.parent
        if output_file_parent_dirpath != parent_output_dirpath:
            self.logger.info(f"Make dir {output_file_parent_dirpath}")
            output_file_parent_dirpath.mkdir(parents=True, exist_ok=True)

    def __open_output_file(self):
        self._output_encoding = self.current_node().get("encoding", None)
        if self._output_encoding == "binary":
            open_mode = "wb"
            encoding = None
        else:
            open_mode = "wt"
            encoding = self._output_encoding
        self._output_stream = open(self.__output_filepath, mode=open_mode, encoding=encoding)

    def post_template_run(self, template_statement: TemplateStatement):
        expected_statement = template_statement.extract_expected_statement()
        self.__output_filepath = expected_statement.current_output_filepath()
        self._output_stream = expected_statement.extract_current_output_stream()
        self.treat_children_nodes()
        self._output_stream.flush()
        self._output_stream.close()
        self._output_stream = None
