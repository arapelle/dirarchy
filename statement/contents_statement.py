import locale
import xml.etree.ElementTree as XMLTree
from io import StringIO

from statement.abstract_contents_statement import AbstractContentsStatement
from statement.abstract_main_statement import AbstractMainStatement


class ContentsStatement(AbstractContentsStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractMainStatement,
                 output_stream=None, output_encoding=None, **kargs):
        if output_stream is None:
            output_stream = StringIO()
            if output_encoding is None:
                output_encoding = locale.getencoding()
        super().__init__(current_node, parent_statement, output_stream, output_encoding, **kargs)

    def allows_template(self):
        return False  # TODO True

    def execute(self):
        self.__write_contents()

    def __write_contents(self):
        copy_attr = self.current_node().attrib.get("copy", None)
        if copy_attr is not None:
            self._copy_file_to_output(copy_attr, self)
        else:
            if "copy-encoding" in self.current_node().attrib:
                raise RuntimeError("'copy-encoding is provided but copy is missing.")
        self.treat_children_nodes()
        self._output_stream.flush()
