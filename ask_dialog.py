import re
from abc import ABC, abstractmethod


class AskDialog(ABC):
    @staticmethod
    def cancel_generation(res=0):
        print("CANCEL!")
        exit(res)

    @abstractmethod
    def _ask_valid_value(self, label: str, default, check_fn=lambda value: len(value) > 0):
        pass

    def ask_valid_bool_value(self, label: str):
        return self._ask_valid_value(label, True,
                                     lambda value: value is not None and isinstance(value, type(True)))

    def ask_valid_int_value(self, label: str, default="0"):
        return self._ask_valid_value(label, default,
                                     lambda value: bool(re.match(r"\A-?\d+\Z", value.strip())))

    def ask_valid_uint_value(self, label: str, default="0"):
        return self._ask_valid_value(label, default,
                                     lambda value: bool(re.match(r"\A\d+\Z", value.strip())))

    def ask_valid_float_value(self, label: str, default="0.0"):
        return self._ask_valid_value(label, default,
                                     lambda value: bool(re.match(r"\A-?\d+(\.\d+)?\Z", value.strip())))

    def ask_valid_var(self, var_type: str, label: str, default=""):
        match var_type:
            case 'int':
                return self.ask_valid_int_value(label, default)
            case 'uint':
                return self.ask_valid_int_value(label, default)
            case 'float':
                return self.ask_valid_float_value(label, default)
            case 'str':
                return self._ask_valid_value(label, default)
            case _:
                raise Exception(f"Bad var_type: '{var_type}'")
