import xml.etree.ElementTree as XMLTree
from abc import ABC

from statement.abstract_main_statement import AbstractMainStatement
from statement.abstract_statement import AbstractStatement
from statement.writer.binary_to_binary_writer import BinaryToBinaryWriter
from statement.writer.binary_to_text_writer import BinaryToTextWriter
from statement.writer.text_to_binary_writer import TextToBinaryWriter
from statement.writer.text_to_text_writer import TextToTextWriter


class AbstractContentsStatement(AbstractMainStatement, ABC):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement,
                 output_stream=None, output_encoding=None, **kargs):
        super().__init__(current_node, parent_statement, **kargs)
        self._output_stream = output_stream
        self._output_encoding = output_encoding

    def extends_template(self):
        return True

    def output_stream(self):
        return self._output_stream

    def output_encoding(self):
        return self._output_encoding

    def current_contents_collector_statement(self):
        return self

    def extract_current_output_stream(self):
        output_stream = self._output_stream
        self._output_stream = None
        return output_stream

    def _copy_file_to_output(self, copy_attr: str, input_statement: AbstractStatement):
        copy_encoding_attr: str = input_statement.current_node().get("copy-encoding", None)
        copied_file_path = self.format_str(copy_attr)
        if copy_encoding_attr is not None:
            input_encoding = self.format_str(copy_encoding_attr)
        else:
            input_encoding = self._output_encoding
        if input_encoding == "binary":
            encoding = None
            mode = "rb"
        else:
            encoding = input_encoding
            mode = "rt"
        with open(copied_file_path, mode=mode, encoding=encoding) as input_file:
            input_contents = input_file.read()
        if self._output_encoding == "binary":
            if input_encoding == "binary":
                writer = BinaryToBinaryWriter(self._output_stream, input_contents, input_statement)
            else:
                writer = TextToBinaryWriter(self._output_stream, input_contents, input_encoding, input_statement)
        else:
            if input_encoding == "binary":
                writer = BinaryToTextWriter(self._output_stream, input_contents, input_statement)
            else:
                writer = TextToTextWriter(self._output_stream, input_contents, input_statement)
        writer.execute()

    def treat_text_of(self, node: XMLTree.Element):
        input_contents = node.text if node.text is not None else ""
        input_contents_len = len(input_contents)
        if input_contents_len > 0:
            if "copy" in node.attrib:
                raise RuntimeError(f"No text is expected when copying a file.")
            if self._output_encoding == "binary":
                writer = TextToBinaryWriter(self._output_stream, input_contents, None, self)
            else:
                writer = TextToTextWriter(self._output_stream, input_contents, self)
            writer.execute()

    def check_number_of_children_nodes_of(self, node: XMLTree.Element):
        if "copy" in self.current_node().attrib and len(node) > 0:
            raise RuntimeError("No child statement is expected when copying a file.")

    def treat_child_node(self, node: XMLTree.Element, child_node: XMLTree.Element):
        match child_node.tag:
            case "if":
                from statement.if_statement import IfStatement
                if_statement = IfStatement(child_node, self)
                if_statement.run()
            case "match":
                from statement.match_statement import MatchStatement
                match_statement = MatchStatement(child_node, self)
                match_statement.run()
            case "random":
                from statement.random_statement import RandomStatement
                random_statement = RandomStatement(child_node, self, self._output_stream)
                random_statement.run()
                self._output_stream = random_statement.io_stream()
            case "contents":
                from statement.contents_statement import ContentsStatement
                contents_statement = ContentsStatement(child_node, self)
                contents_statement.run()
            case _:
                super().treat_child_node(node, child_node)
