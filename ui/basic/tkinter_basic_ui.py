from ui.basic.abstract_basic_ui import AbstractBasicUi
from ui.basic.string_check import AbstractStringCheck


class TkinterBasicUi(AbstractBasicUi):
    NAME = "TKINTER"

    def __init__(self):
        import tkinter
        self.__gui = tkinter.Tk()
        self.__gui.withdraw()

    @staticmethod
    def __ask_str_value(label: str, default_value: str, error_msg=None):
        from tkinter import simpledialog
        error_msg = f"{error_msg}\n\n" if error_msg is not None else ""
        return simpledialog.askstring(label, f"{error_msg}{label}: ", initialvalue=default_value)

    @staticmethod
    def __ask_bool_value(label: str):
        from tkinter import messagebox
        return messagebox.askyesnocancel(label, label)

    def ask_valid_bool(self, label: str, default_value):
        value = self.__ask_bool_value(label)
        if value is None:
            self.raise_cancel()
        print(f"{label}: '{value}'")
        return str(value)

    def ask_valid_string(self, label: str, default, str_check: AbstractStringCheck | None = None):
        error_msg = None
        while True:
            value = self.__ask_str_value(label, default, error_msg)
            if value is None:
                self.raise_cancel()
            print(f"{label}: '{value}'")
            if str_check is None:
                return value
            valid, error_msg = str_check.check(value)
            if valid:
                return value
