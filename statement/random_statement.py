import random
import xml.etree.ElementTree as XMLTree
from builtins import RuntimeError
from io import IOBase

import random_string
from log import MethodScopeLog
from statement.abstract_main_statement import AbstractMainStatement
from statement.abstract_statement import AbstractStatement


class RandomStatement(AbstractMainStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, io_stream: IOBase, **kargs):
        super().__init__(current_node, parent_statement, **kargs)
        self.__io_stream = io_stream

    def io_stream(self):
        return self.__io_stream

    def run(self):
        with MethodScopeLog(self):
            self.treat_children_nodes_of(self.current_node())
            random_node = self.current_node()
            value_type = random_node.attrib.get("type", None)
            if value_type:
                match value_type:
                    case 'int':
                        random_value = self.__random_int_string(random_node)
                        self.__io_stream.write(random_value)
                        return
                    case 'float':
                        random_value = self.__random_float_string(random_node)
                        self.__io_stream.write(random_value)
                        return
                    case 'format_cvqd':
                        random_value = self.__random_format_cvqd(random_node)
                        self.__io_stream.write(random_value)
                        return
                rand_fn_name = f"random_{value_type}_string"
                try:
                    rand_fn = getattr(random_string, rand_fn_name)
                    min_len = int(random_node.attrib.get("min-len"))
                    max_len = int(random_node.attrib.get("max-len"))
                    random_value = rand_fn(min_len, max_len)
                    self.__io_stream.write(random_value)
                except AttributeError:
                    raise RuntimeError(f"Bad value type: '{value_type}'.")
            else:
                char_set = random_node.attrib.get("char-set")
                min_len = int(random_node.attrib.get("min-len"))
                max_len = int(random_node.attrib.get("max-len"))
                random_value = random_string.random_string(char_set, min_len, max_len)
                self.__io_stream.write(random_value)

    @staticmethod
    def __random_int_string(rand_value_node: XMLTree.Element):
        min_value = int(rand_value_node.attrib.get("min"))
        max_value = int(rand_value_node.attrib.get("max"))
        return str(random.randint(min_value, max_value))

    @staticmethod
    def __random_float_string(rand_value_node: XMLTree.Element):
        min_value = float(rand_value_node.attrib.get("min"))
        max_value = float(rand_value_node.attrib.get("max"))
        return f"{random.uniform(min_value, max_value):.3f}"

    @staticmethod
    def __random_format_cvqd(rand_value_node: XMLTree.Element):
        fmt_str = rand_value_node.attrib.get("fmt")
        return random_string.random_format_cvqd_string(fmt_str)
