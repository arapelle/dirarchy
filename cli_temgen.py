import argparse
from enum import StrEnum, auto
from pathlib import Path
import re

import constants
import temgen
import regex
from ui.tkinter_ui import TkinterUi
from ui.terminal_ui import TerminalUi


class CliTemgen(temgen.Temgen):
    class UiType(StrEnum):
        TKINTER = auto()
        TERMINAL = auto()

    def __init__(self, argv=None):
        self._args = self._parse_args(argv)
        super().__init__(self.__build_ui_from_args())
        self.__init_variables_from_args()

    @property
    def args(self):
        return self._args

    def _parse_args(self, argv=None):
        prog_name = constants.PROGRAM_NAME
        prog_desc = 'A tool generating a directory architecture based on a template.'
        argparser = argparse.ArgumentParser(prog=prog_name, description=prog_desc)
        argparser.add_argument('--version', action='version',
                               version=f'{prog_name} {temgen.Temgen.VERSION}')
        argparser.add_argument('-K', f'--{CliTemgen.UiType.TKINTER}'.lower(), action='store_const',
                               dest='ui', const=CliTemgen.UiType.TKINTER, help='Use tkinter I/O.')
        argparser.add_argument('-T', f'--{CliTemgen.UiType.TERMINAL}'.lower(), action='store_const',
                               dest='ui', const=CliTemgen.UiType.TERMINAL, default='terminal',
                               help='Use terminal I/O.')
        argparser.add_argument('-C', '--custom-ui', metavar='custom_ui_cmd',
                               help='Use a custom user interface to set variables before treating them with temgen. '
                                    '(Executing custom_ui_cmd in shell is expected to use the desired custom '
                                    'interface.)')
        argparser.add_argument('-o', '--output-dir', metavar='dir_path',
                               default=Path.cwd(),
                               help='The directory where to generate the desired hierarchy (dir or file).')
        argparser.add_argument('-v', '--var', metavar='key=value', nargs='+',
                               type=CliTemgen.__var_from_key_value_str,
                               help='Set variables.')
        argparser.add_argument('--var-file', metavar='var_json_files', nargs='+',
                               help='Set variables from a JSON files.')
        argparser.add_argument('template_path',
                               help='The template path of the file to find then to process.')
        argparser.add_argument('template_version', nargs='?',
                               help='The template version.')
        args = argparser.parse_args(argv)
        if args.ui is None:
            args.ui = CliTemgen.UiType.TKINTER
        args.output_dir = Path(args.output_dir)
        return args

    @classmethod
    def __var_from_key_value_str(cls, key_value_str: str):
        key, value = key_value_str.split('=')
        if re.match(regex.VAR_NAME_REGEX, key):
            return key, value
        raise RuntimeError(key_value_str)

    def __build_ui_from_args(self):
        match self.args.ui:
            case CliTemgen.UiType.TERMINAL:
                ui = TerminalUi()
            case CliTemgen.UiType.TKINTER:
                ui = TkinterUi()
            case _:
                raise Exception(f"Unknown I/O: '{self.args.io}'")
        return ui

    def __init_variables_from_args(self):
        if self.args.var:
            self.init_variables().update_vars_from_dict(self.args.var)
        if self.args.var_file:
            self.init_variables().update_vars_from_files(self.args.var_file)
        if self.args.custom_ui:
            self.init_variables().update_vars_from_custom_ui(self.args.custom_ui)

    def run(self):
        self.find_and_treat_template_file(Path(self.args.template_path),
                                          self.args.template_version,
                                          output_dir=self.args.output_dir)


if __name__ == '__main__':
    cli_temgen = CliTemgen()
    cli_temgen.run()
