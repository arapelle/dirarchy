from ask_dialog import AskDialog


class GuiAskDialog(AskDialog):
    def __init__(self):
        import tkinter
        self.__gui = tkinter.Tk()
        self.__gui.withdraw()

    def __ask_str_value(self, label: str, default: str, prev_value=None):
        from tkinter import simpledialog
        prev_value = f"BAD ENTRY: \"{prev_value}\"\n" if prev_value is not None else ""
        return simpledialog.askstring(label, f"{prev_value}{label}: ", initialvalue=default)

    def __ask_bool_value(self, label: str):
        from tkinter import messagebox
        return messagebox.askyesnocancel(label, label)

    def _ask_valid_value(self, label: str, default, check_fn=lambda value: len(value) > 0):
        value_is_bool = isinstance(default, type(True))
        value = None if value_is_bool else ""
        prev_value = None
        while not check_fn(value):
            if value_is_bool:
                value = self.__ask_bool_value(label)
            else:
                value = self.__ask_str_value(label, default, prev_value)
            if value is None:
                self.cancel_generation()
            print(f"Parameter '{label}': '{value}'")
            prev_value = value
        return value
