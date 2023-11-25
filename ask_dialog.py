import re
from abc import ABC, abstractmethod


class AskDialog(ABC):
    @staticmethod
    def raise_cancel(res=0):
        print("CANCEL!")
        exit(res)

    @abstractmethod
    def ask_valid_bool(self, label: str, default_value):
        pass

    @abstractmethod
    def ask_valid_string(self, label: str, default_value, check_fn):
        pass

    def ask_valid_printable_string(self, label: str, default_value, check_fn):
        def __check_printable_str(value):
            return len(value) > 0 and (check_fn is None or check_fn(value))

        return self.ask_valid_string(label, default_value, __check_printable_str)

    def ask_valid_graphic_string(self, label: str, default_value, check_fn):
        def __check_graphic_str(value):
            value = value.strip()
            return len(value) > 0 and (check_fn is None or check_fn(value))

        return self.ask_valid_string(label, default_value, __check_graphic_str).strip()

    def ask_valid_int(self, label: str, default_value="0", check_fn=None):
        def __check_int(value):
            value = value.strip()
            return bool(re.match(r"\A-?\d+\Z", value)) and (check_fn is None or check_fn(value))

        return self.ask_valid_string(label, default_value, __check_int).strip()

    def ask_valid_uint(self, label: str, default_value="0", check_fn=None):
        def __check_uint(value):
            value = value.strip()
            return bool(re.match(r"\A\d+\Z", value)) and (check_fn is None or check_fn(value))

        return self.ask_valid_string(label, default_value, __check_uint).strip()

    def ask_valid_float(self, label: str, default_value="0.0", check_fn=None):
        def __check_float(value):
            value = value.strip()
            return bool(re.match(r"\A-?\d+(\.\d+)?\Z", value)) and (check_fn is None or check_fn(value))

        return self.ask_valid_string(label, default_value, __check_float).strip()

    def ask_valid_var(self, var_type: str, label: str, default_value=None, check_fn=None):
        match var_type:
            case 'bool':
                return self.ask_valid_bool(label, default_value)
            case 'int':
                return self.ask_valid_int(label, default_value, check_fn)
            case 'uint':
                return self.ask_valid_int(label, default_value, check_fn)
            case 'float':
                return self.ask_valid_float(label, default_value, check_fn)
            case 'str':
                return self.ask_valid_string(label, default_value, check_fn)
            case 'pstr':
                return self.ask_valid_string(label, default_value, check_fn)
            case 'gstr':
                return self.ask_valid_graphic_string(label, default_value, check_fn)
            case _:
                raise Exception(f"Bad var_type: '{var_type}'")
