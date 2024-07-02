import locale
import re
import xml.etree.ElementTree as XMLTree
from builtins import RuntimeError
from io import StringIO

from constants import regex
from statement.abstract_contents_statement import AbstractContentsStatement
from statement.abstract_statement import AbstractStatement


class RegexFullMatch:
    def __init__(self, regex_pattern):
        if isinstance(regex_pattern, re.Pattern):
            self.__regex = regex_pattern
        else:
            self.__regex = re.compile(regex_pattern)

    def __call__(self, value_to_check: str):
        return re.fullmatch(self.__regex, value_to_check)


class VarStatement(AbstractContentsStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, ui_variables=None, **kargs):
        super().__init__(current_node, parent_statement, variables=parent_statement.variables(), **kargs)
        self.__var_name = None
        self.__var_type = None
        self.__var_default = None
        self.__var_regex = None
        self.__var_value = None
        self.__ui_variables = ui_variables

    def execute(self):
        var_node = self.current_node()
        self.__var_name = var_node.attrib.get('name')
        if not re.match(regex.VAR_NAME_REGEX, self.__var_name):
            raise Exception(f"Variable name is not a valid name: '{self.__var_name}'.")
        self.__var_type = var_node.attrib.get('type', 'str')
        var_restr = var_node.attrib.get('regex', None)
        self.__var_regex = RegexFullMatch(var_restr) if var_restr is not None else None
        self.__resolve_var_value(var_node)
        self.__check_variable_value()
        self.variables().update_var_and_log(self.__var_name, self.__var_value)

    def __resolve_var_value(self, var_node):
        copy_attr = self.current_node().attrib.get("copy", None)
        if copy_attr is not None:
            self.__resolve_var_value_with_file(copy_attr)
            if 'value' in var_node.attrib:
                raise RuntimeError("Incompatible 'value' attribute with 'copy' attribute.")
            return
        if "copy-encoding" in self.current_node().attrib:
            raise RuntimeError("'copy-encoding is provided but copy is missing.")
        self.__var_value = self.variables().get(self.__var_name, None)
        if self.__var_value is not None:  # or if value is not compatible with requirements (type, regex, ...).
            self.__var_value = self.vformat_with_format_attr(self.__var_value)
            return
        self.__var_value = var_node.attrib.get('value', None)
        if self.__var_value is not None:  # or if value is not compatible with requirements (type, regex, ...).
            if var_node.text is not None and len(var_node.text) > 0:
                raise RuntimeError("For 'var', you cannot provide value and text at the same time.")
            if len(var_node) > 0:
                raise RuntimeError("No child statement is expected when using value attribute.")
            self.__var_value = self.vformat_with_format_attr(self.__var_value)
            return
        self.__var_value = self.get_variable_value(self.__var_name)
        if self.__var_value is not None:  # or if value is not compatible with requirements (type, regex, ...).
            return
        if self.__ui_variables is not None:
            self.__var_value = self.__ui_variables.get(self.__var_name, None)
            if self.__var_value is not None:  # or if value is not compatible with requirements (type, regex, ...).
                return
        if len(var_node) == 0 and (var_node.text is None or len(var_node.text) == 0):
            self.__manage_unset_var_value(var_node)
        else:
            self.__resolve_var_value_with_text_or_children()

    def __manage_unset_var_value(self, var_node):
        if_unset_attr = var_node.get("if-unset", "ask")
        if_unset_attr = self.vformat(if_unset_attr)
        match if_unset_attr:
            case "ask":
                self.__ask_var_value(var_node)
            case "use-default":
                self.__use_default_value(var_node)
            case "error":
                assert self.__var_value is None
                raise RuntimeError(f"The variable '{self.__var_name}' is not set.")
            case _:
                raise RuntimeError(f"Unknown action '{if_unset_attr}' to manage the unset variable "
                                   f"'{self.__var_name}'.")

    def __resolve_var_value_with_file(self, copy_attr):
        self.__make_output_stream()
        self._copy_file_to_output(copy_attr, self)
        self.__var_value = self._output_stream.getvalue()

    def __ask_var_value(self, var_node):
        self.__var_default = var_node.attrib.get('default', None)
        if self.__var_default is not None:
            self.__var_default = self.vformat(self.__var_default)
        self.__var_value = self.temgen().basic_ui().ask_valid_var(self.__var_type, self.__var_name,
                                                                  self.__var_default, self.__var_regex)

    def __use_default_value(self, var_node):
        self.__var_default = var_node.attrib.get('default', None)
        if self.__var_default is not None:
            self.__var_default = self.vformat(self.__var_default)
        else:
            match self.__var_type:
                case 'bool':
                    self.__var_default = "False"
                case 'int' | 'uint':
                    self.__var_default = "0"
                case 'float':
                    self.__var_default = "0.0"
                case 'str':
                    self.__var_default = ""
                case _:
                    raise RuntimeError(f"Action 'use-default' is chosen for the unset variable '{self.__var_name} of "
                                       f"type '{self.__var_type}', but the default value is missing "
                                       f"(use attribute 'default').")
        self.__var_value = self.__var_default

    def __resolve_var_value_with_text_or_children(self):
        self.__make_output_stream()
        self.treat_children_nodes()
        self.__var_value = self._output_stream.getvalue()

    def __make_output_stream(self):
        match self.__var_type:
            case "str" | "pstr" | "gstr" | "int" | "float":
                self._output_stream = StringIO()
                self._output_encoding = locale.getencoding()
            case _:
                raise RuntimeError(f"Bad type {self.__var_type}")

    def __check_variable_value(self):
        # TODO use self.__var_type and self.__var_regex (if any), to check self.__var_value
        pass

    def check_number_of_children_nodes_of(self, node: XMLTree.Element):
        if len(node) > 1:
            raise RuntimeError(f"Too many nodes for <{node.tag}>.")
        super().check_number_of_children_nodes_of(node)
