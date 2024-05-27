from ui.terminal_ui import TerminalUi
from ui.tkinter_ui import TkinterUi


def make_ui_from_name(ui_name: str):
    match ui_name:
        case TerminalUi.NAME:
            ui = TerminalUi()
        case TkinterUi.NAME:
            ui = TkinterUi()
        case _:
            ui = None
    return ui
