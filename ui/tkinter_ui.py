from ui.abstract_ui import AbstractBasicUi


class TkinterBasicUi(AbstractBasicUi):
    NAME = "TKINTER"

    def __init__(self):
        import tkinter
        self.__gui = tkinter.Tk()
        self.__gui.withdraw()

    @staticmethod
    def __ask_str_value(label: str, default_value: str, prev_value=None):
        from tkinter import simpledialog
        prev_value = f"BAD ENTRY: \"{prev_value}\"\n" if prev_value is not None else ""
        return simpledialog.askstring(label, f"{prev_value}{label}: ", initialvalue=default_value)

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

    def ask_valid_string(self, label: str, default, check_fn):
        prev_value = None
        while True:
            value = self.__ask_str_value(label, default, prev_value)
            if value is None:
                self.raise_cancel()
            print(f"{label}: '{value}'")
            if check_fn is None or check_fn(value):
                return value
            prev_value = value
