from abc import ABC, abstractmethod

from ui.basic.string_check import AbstractStringCheck, GraphicStringCheck, IntStringCheck, UintStringCheck, \
    FloatStringCheck


class AbstractBasicUi(ABC):
    @staticmethod
    def raise_cancel(res=0):
        print("CANCEL!")
        exit(res)

    @abstractmethod
    def ask_valid_bool(self, label: str, default_value):
        pass

    @abstractmethod
    def ask_valid_string(self, label: str, default_value, str_check: AbstractStringCheck | None = None):
        pass

    def ask_valid_graphic_string(self, label: str, default_value, str_check: AbstractStringCheck | None = None):
        str_check = GraphicStringCheck(next=str_check)
        return self.ask_valid_string(label, default_value, str_check)

    def ask_valid_int(self, label: str, default_value="0", str_check: AbstractStringCheck | None = None):
        str_check = IntStringCheck(next=str_check)
        return self.ask_valid_string(label, default_value, str_check).strip()

    def ask_valid_uint(self, label: str, default_value="0", str_check: AbstractStringCheck | None = None):
        str_check = UintStringCheck(next=str_check)
        return self.ask_valid_string(label, default_value, str_check).strip()

    def ask_valid_float(self, label: str, default_value="0.0", str_check: AbstractStringCheck | None = None):
        str_check = FloatStringCheck(next=str_check)
        return self.ask_valid_string(label, default_value, str_check).strip()

    def ask_valid_var(self, var_type: str, label: str, default_value=None,
                      str_check: AbstractStringCheck | None = None):
        match var_type:
            case 'bool':
                return self.ask_valid_bool(label, default_value)
            case 'int':
                return self.ask_valid_int(label, default_value, str_check)
            case 'uint':
                return self.ask_valid_uint(label, default_value, str_check)
            case 'float':
                return self.ask_valid_float(label, default_value, str_check)
            case 'str':
                return self.ask_valid_string(label, default_value, str_check)
            case 'gstr':
                return self.ask_valid_graphic_string(label, default_value, str_check)
            case _:
                raise RuntimeError(f"Bad var_type: '{var_type}'")
