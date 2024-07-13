from ui.basic.abstract_basic_ui import AbstractBasicUi
from ui.basic.string_check import AbstractStringCheck


class TerminalBasicUi(AbstractBasicUi):
    NAME = "TERMINAL"

    @staticmethod
    def __ask_str_value(prompt: str, error_msg=None):
        try:
            if error_msg is not None:
                print(error_msg)
            return input(f"{prompt}: ")
        except KeyboardInterrupt:
            return None

    @staticmethod
    def __ask_bool_value(prompt: str, default_value, cancel_enabled):
        try:
            read_value = input(f"{prompt}: ")
            if read_value == '' and default_value is not None:
                read_value = 'y' if default_value else 'n'
            match read_value:
                case 'y' | 'Y':
                    return str(True)
                case 'n' | 'N':
                    return str(False)
                case 'c' | 'C':
                    if cancel_enabled:
                        return None
                case _:
                    return read_value
        except KeyboardInterrupt:
            return None

    def ask_valid_bool(self, prompt: str, default_value, cancel_enabled=False):
        assert default_value is None or eval(default_value)
        y_val = 'y'
        n_val = 'n'
        if default_value is not None:
            y_val = 'Y' if eval(default_value) is True else 'y'
            n_val = 'N' if eval(default_value) is False else 'n'
        prompt = f"{prompt} ({y_val}/{n_val}/c)" if cancel_enabled else f"{prompt} ({y_val}/{n_val}"
        read_value = None
        while True:
            read_value = self.__ask_bool_value(prompt, default_value, cancel_enabled)
            if read_value is None:
                self.raise_cancel()
            if read_value == 'True' or read_value == 'False':
                return read_value

    def ask_valid_string(self, prompt: str, default_value, str_check: AbstractStringCheck | None = None):
        import importlib.util
        readline_spec = importlib.util.find_spec("readline")
        if readline_spec is not None:
            import readline
        if not (default_value is None or str_check is None or str_check.check(default_value)[0]):
            raise RuntimeError(f"The default value is None or it is not a valid entry: {default_value}.")
        if default_value is not None:
            prompt = f"{prompt} (default: {default_value})"
        read_value = None
        error_msg = None
        while True:
            read_value = self.__ask_str_value(prompt, error_msg)
            if read_value is None:
                self.raise_cancel()
            if str_check is None:
                return read_value
            valid, error_msg = str_check.check(read_value)
            if valid:
                return read_value
            if default_value is not None and len(read_value) == 0:
                print(f"  default used: {default_value}")
                return default_value
