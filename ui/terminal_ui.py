from ui.abstract_ui import AbstractUi


class TerminalUi(AbstractUi):
    @staticmethod
    def __ask_str_value(prompt: str, prev_value=None):
        try:
            if prev_value is not None:
                print(f"BAD ENTRY: \"{prev_value}\"")
            return input(f"{prompt}: ")
        except KeyboardInterrupt:
            return None

    @staticmethod
    def __ask_bool_value(prompt: str, default_value):
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
                    return None
                case _:
                    return read_value
        except KeyboardInterrupt:
            return None

    def ask_valid_bool(self, prompt: str, default_value):
        assert default_value is None or eval(default_value)
        y_val = 'y'
        n_val = 'n'
        if default_value is not None:
            y_val = 'Y' if eval(default_value) is True else 'y'
            n_val = 'N' if eval(default_value) is False else 'n'
        prompt = f"{prompt} ({y_val}/{n_val}/c)"
        read_value = None
        while True:
            read_value = self.__ask_bool_value(prompt, default_value)
            if read_value is None:
                self.raise_cancel()
            if read_value == 'True' or read_value == 'False':
                return read_value

    def ask_valid_string(self, prompt: str, default_value, check_fn):
        assert default_value is None or check_fn is None or check_fn(default_value)
        if default_value is not None:
            prompt = f"{prompt} (default: {default_value})"
        read_value = None
        prev_value = None
        while True:
            read_value = self.__ask_str_value(prompt, prev_value)
            if read_value is None:
                self.raise_cancel()
            if check_fn is None or check_fn(read_value):
                return read_value
            if default_value is not None and len(read_value) == 0:
                print(f"  default: {default_value}.")
                return default_value
            prev_value = read_value
