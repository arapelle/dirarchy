from ui.basic.terminal_basic_ui import TerminalBasicUi
from ui.basic.tkinter_basic_ui import TkinterBasicUi


def make_basic_ui_from_name(ui_name: str):
    match ui_name:
        case TerminalBasicUi.NAME:
            ui = TerminalBasicUi()
        case TkinterBasicUi.NAME:
            ui = TkinterBasicUi()
        case _:
            ui = None
    return ui
