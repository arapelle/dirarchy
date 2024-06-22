import argparse
from pathlib import Path
import re

import temgen
from constants import regex, names
from ui.make_ui_from_name import make_ui_from_name
from ui.terminal_ui import TerminalBasicUi
from ui.tkinter_ui import TkinterBasicUi


class CliTemgen(temgen.Temgen):
    def __init__(self, argv=None):
        self._args = self._parse_args(argv)
        super().__init__(make_ui_from_name(self.args.basic_ui),
                         var_dict=self.args.var if self.args.var else [],
                         var_files=self.args.var_file if self.args.var_file else [],
                         ui=self.args.ui)

    @property
    def args(self):
        return self._args

    def _parse_args(self, argv=None):
        prog_name = names.PROGRAM_NAME
        prog_desc = 'A tool generating a directory architecture based on a template.'
        argparser = argparse.ArgumentParser(prog=prog_name, description=prog_desc)
        argparser.add_argument('--version', action='version',
                               version=f'{prog_name} {temgen.Temgen.VERSION}')
        argparser.add_argument('-K', f'--{TkinterBasicUi.NAME}'.lower(), action='store_const',
                               dest='basic_ui', const=TkinterBasicUi.NAME, help='Use tkinter I/O.')
        argparser.add_argument('-T', f'--{TerminalBasicUi.NAME}'.lower(), action='store_const',
                               dest='basic_ui', const=TerminalBasicUi.NAME, default='terminal',
                               help='Use terminal I/O.')
        argparser.add_argument('-U', '--ui', metavar='ui_cmd',
                               help='Use a custom user interface to set variables before treating them with temgen. '
                                    '(Executing ui_cmd in shell is expected to use the desired custom interface.)')
        argparser.add_argument('-o', '--output-dir', metavar='dir_path',
                               default=Path.cwd(),
                               help='The directory where to generate the desired hierarchy (dir or file).')
        argparser.add_argument('-v', '--var', metavar='key=value', nargs='+',
                               type=CliTemgen.__var_from_key_value_str,
                               help='Set variables.')
        argparser.add_argument('--var-file', metavar='var_json_file', nargs='+',
                               help='Set variables from a JSON files.')
        argparser.add_argument('template_path',
                               help='The template path of the file to find then to process.')
        argparser.add_argument('template_version', nargs='?',
                               help='The template version.')
        args = argparser.parse_args(argv)
        args.output_dir = Path(args.output_dir)
        return args

    @classmethod
    def __var_from_key_value_str(cls, key_value_str: str):
        key, value = key_value_str.split('=')
        if re.match(regex.VAR_NAME_REGEX, key):
            return key, value
        raise RuntimeError(key_value_str)

    def run(self):
        self.find_and_treat_template_file(Path(self.args.template_path),
                                          self.args.template_version,
                                          output_dir=self.args.output_dir)


if __name__ == '__main__':
    cli_temgen = CliTemgen()
    cli_temgen.run()
