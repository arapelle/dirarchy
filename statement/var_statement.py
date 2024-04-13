import locale
import re
import xml.etree.ElementTree as XMLTree
from builtins import RuntimeError
from io import StringIO, BytesIO

import regex
from statement.abstract_contents_statement import AbstractContentsStatement
from statement.abstract_statement import AbstractStatement
from statement.random_statement import RandomStatement


class RegexFullMatch:
    def __init__(self, regex_pattern):
        if isinstance(regex_pattern, re.Pattern):
            self.__regex = regex_pattern
        else:
            self.__regex = re.compile(regex_pattern)

    def __call__(self, value_to_check: str):
        return re.fullmatch(self.__regex, value_to_check)


class VarStatement(AbstractContentsStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, **kargs):
        super().__init__(current_node, parent_statement, None, None, variables=parent_statement.variables(), **kargs)
        self.__var_name = None
        self.__var_type = None
        self.__var_default = None
        self.__var_regex = None
        self.__var_value = None

    def execute(self):
        var_node = self.current_node()
        self.__var_name = var_node.attrib.get('name')
        if not re.match(regex.VAR_NAME_REGEX, self.__var_name):
            raise Exception(f"Variable name is not a valid name: '{self.__var_name}'.")
        self.__var_value = self.get_variable_value(self.__var_name)
        self.__var_type = var_node.attrib.get('type', 'str')
        var_restr = var_node.attrib.get('regex', None)
        self.__var_regex = RegexFullMatch(var_restr) if var_restr is not None else None
        if self.__var_value is None:
            self.__resolve_var_value(var_node)
        else:
            self.__check_variable_value()

    def __resolve_var_value(self, var_node):
        copy_attr = self.current_node().attrib.get("copy", None)
        if copy_attr is not None:
            self.__resolve_var_value_with_file(copy_attr)
        else:
            if "copy-encoding" in self.current_node().attrib:
                raise RuntimeError("'copy-encoding is provided but copy is missing.")
            self.__var_value = var_node.attrib.get('value', None)
            if self.__var_value is None:
                if len(var_node) == 0 and (var_node.text is None or len(var_node.text) == 0):
                    self.__ask_var_value(var_node)
                else:
                    self.__resolve_var_value_with_text_or_children()
            else:
                if var_node.text is not None and len(var_node.text) > 0:
                    raise RuntimeError("For 'var', you cannot provide value and text at the same time.")
                if len(var_node) > 0:
                    raise RuntimeError("No child statement is expected when using value attribute.")
            self.__var_value = self.format_str(self.__var_value)
        self.__check_variable_value()
        self.variables().update_var_and_log(self.__var_name, self.__var_value)

    def __resolve_var_value_with_file(self, copy_attr):
        self.__make_output_stream()
        self._copy_file_to_output(copy_attr, self)
        self.__var_value = self._output_stream.getvalue()

    def __ask_var_value(self, var_node):
        self.__var_default = var_node.attrib.get('default', None)
        self.__var_value = self.temgen().ui().ask_valid_var(self.__var_type, self.__var_name,
                                                            self.__var_default, self.__var_regex)

    def __resolve_var_value_with_text_or_children(self):
        self.__make_output_stream()
        self.treat_children_nodes()
        self.__var_value = self._output_stream.getvalue()

    def __make_output_stream(self):
        match self.__var_type:
            case "str" | "pstr" | "gstr" | "int" | "float":
                self._output_stream = StringIO()
                self._output_encoding = locale.getencoding()
            case "binary":
                self._output_stream = BytesIO()
                self._output_encoding = "binary"
            case _:
                raise RuntimeError(f"Bad type {self.__var_type}")

    def __check_variable_value(self):
        # TODO use self.__var_type and self.__var_regex (if any), to check self.__var_value
        pass

    def check_number_of_children_nodes_of(self, node: XMLTree.Element):
        if len(node) > 1:
            raise RuntimeError(f"Too many nodes for <{node.tag}>.")
        super().check_number_of_children_nodes_of(node)

    def treat_child_node(self, node: XMLTree.Element, child_node: XMLTree.Element):
        match child_node.tag:
            case "random":
                random_statement = RandomStatement(child_node, self, self._output_stream)
                random_statement.run()
                self._output_stream = random_statement.io_stream()
            case _:
                super().treat_child_node(node, child_node)
