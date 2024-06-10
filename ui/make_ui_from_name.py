from ui.terminal_ui import TerminalBasicUi
from ui.tkinter_ui import TkinterBasicUi


def make_ui_from_name(ui_name: str):
    match ui_name:
        case TerminalBasicUi.NAME:
            ui = TerminalBasicUi()
        case TkinterBasicUi.NAME:
            ui = TkinterBasicUi()
        case _:
            ui = None
    return ui
