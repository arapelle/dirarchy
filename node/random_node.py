import random
import xml.etree.ElementTree as XMLTree

import random_string


class RandomNode:
    @staticmethod
    def random_string(random_node: XMLTree.Element):
        value_type = random_node.attrib.get("type", None)
        if value_type:
            match value_type:
                case 'int':
                    return RandomNode.__random_int_string(random_node)
                case 'float':
                    return RandomNode.__random_float_string(random_node)
                case 'format_cvqd':
                    return RandomNode.__random_format_cvqd(random_node)
            rand_fn_name = f"random_{value_type}_string"
            try:
                rand_fn = getattr(random_string, rand_fn_name)
                min_len = int(random_node.attrib.get("min-len"))
                max_len = int(random_node.attrib.get("max-len"))
                return rand_fn(min_len, max_len)
            except AttributeError:
                raise RuntimeError(f"Bad value type: '{value_type}'.")
        else:
            char_set = random_node.attrib.get("char-set")
            min_len = int(random_node.attrib.get("min-len"))
            max_len = int(random_node.attrib.get("max-len"))
            return random_string.random_string(char_set, min_len, max_len)

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
