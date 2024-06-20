import random
import xml.etree.ElementTree as XMLTree
from builtins import RuntimeError
from io import IOBase, StringIO, BytesIO

from util import random_string
from statement.abstract_main_statement import AbstractMainStatement
from statement.abstract_statement import AbstractStatement


class RandomStatement(AbstractMainStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement,
                 io_stream: IOBase | None, **kargs):
        super().__init__(current_node, parent_statement, **kargs)
        self.__io_stream = io_stream

    def io_stream(self):
        return self.__io_stream

    def execute(self):
        random_value = self.__try_random_value_from_type()
        if random_value is None:
            random_value = self.__try_random_value_from_set()
        if random_value is not None:
            self.__io_stream.write(random_value)
        else:
            raise RuntimeError("One of the following attribute is missing for random statement: "
                               "type, char-set, byte-set.")

    def __build_string_stream_if_missing(self):
        if self.__io_stream is None:
            self.__io_stream = StringIO()

    def __build_bytes_stream_if_missing(self):
        if self.__io_stream is None:
            self.__io_stream = BytesIO()

    def __try_random_value_from_type(self):
        value_type = self.current_node().attrib.get("type", None)
        match value_type:
            case None:
                return None
            case "binary":
                self.__build_bytes_stream_if_missing()
                return self.random_bytes(self.current_node())
            case _:
                self.__build_string_stream_if_missing()
        rand_fn_name = f"random_{value_type}_string"
        try:
            rand_fn = getattr(self, rand_fn_name)
            return rand_fn(self.current_node())
        except AttributeError:
            pass
        try:
            rand_fn = getattr(random_string, rand_fn_name)
            max_len, min_len = self.__get_min_max_len(self.current_node())
            return rand_fn(min_len, max_len)
        except AttributeError:
            raise RuntimeError(f"Bad value type: '{value_type}'.")

    def __try_random_value_from_set(self):
        max_len, min_len = self.__get_min_max_len(self.current_node())
        element_set = self.current_node().attrib.get("char-set", None)
        if element_set is not None:
            self.__build_string_stream_if_missing()
            return random_string.random_string(element_set, min_len, max_len)
        element_set = self.current_node().attrib.get("byte-set", None)
        if element_set is not None:
            self.__build_bytes_stream_if_missing()
            return self.random_selected_bytes(element_set, min_len, max_len)
        return None

    @staticmethod
    def __get_min_max_len(random_node):
        length = random_node.attrib.get("len", None)
        if length is not None:
            length = int(length)
            return length, length
        min_len = int(random_node.attrib.get("min-len", 0))
        max_len = int(random_node.attrib.get("max-len"))
        if min_len > max_len:
            raise RuntimeError(f"In random, min-len ({min_len}) must be less than max-len ({max_len}).")
        return max_len, min_len

    @staticmethod
    def random_int_string(rand_value_node: XMLTree.Element):
        min_value = int(rand_value_node.attrib.get("min", 0))
        max_value = int(rand_value_node.attrib.get("max"))
        if min_value > max_value:
            raise RuntimeError(f"In random, min ({min_value}) must be less than max ({max_value}).")
        return str(random.randint(min_value, max_value))

    @staticmethod
    def random_float_string(rand_value_node: XMLTree.Element):
        min_value = float(rand_value_node.attrib.get("min", 0))
        max_value = float(rand_value_node.attrib.get("max"))
        if min_value > max_value:
            raise RuntimeError(f"In random, min ({min_value}) must be less than max ({max_value}).")
        return f"{random.uniform(min_value, max_value):.3f}"

    @staticmethod
    def random_format_cvqd_string(rand_value_node: XMLTree.Element):
        fmt_str = rand_value_node.attrib.get("fmt")
        return random_string.random_format_cvqd_string(fmt_str)

    @staticmethod
    def random_bytes(rand_value_node: XMLTree.Element):
        max_len, min_len = RandomStatement.__get_min_max_len(rand_value_node)
        s_len = min_len if max_len is None else random.randint(min_len, max_len)
        assert s_len >= 0
        return random.randbytes(s_len)

    @staticmethod
    def random_selected_bytes(byte_set, min_len: int, max_len=None):
        s_len = min_len if max_len is None else random.randint(min_len, max_len)
        assert s_len >= 0
        byte_set = byte_set.split(',')
        byte_set = [int(sval) for sval in byte_set]
        return b''.join(bytes([random.choice(byte_set)]) for i in range(s_len))
