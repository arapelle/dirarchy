import re
from pathlib import Path

import temgen
from constants import regex
from ui.basic.make_basic_ui_from_name import make_basic_ui_from_name
from ui.basic.terminal_basic_ui import TerminalBasicUi
from ui.basic.tkinter_basic_ui import TkinterBasicUi
from util.cli_command import CliCommand


class Generate(CliCommand):
    def __init__(self, parent: CliCommand, subparsers):
        description = "Generate a directory architecture based on a template."
        super().__init__(parent, subparsers=subparsers,
                         description=description,
                         help=description)
        argparser = self.arg_parser()
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
                               type=self.__var_from_key_value_str,
                               help='Set variables.')
        argparser.add_argument('--var-file', metavar='var_json_file', nargs='+',
                               help='Set variables from a JSON files.')
        argparser.add_argument("--check-template", help="Check the names of all statements and their attributes.",
                               action="store_true")
        argparser.add_argument('template_path',
                               help='The template path of the file to find then to process.')
        argparser.add_argument('template_version', nargs='?',
                               help='The template version.')

    @classmethod
    def __var_from_key_value_str(cls, key_value_str: str):
        key, value = key_value_str.split('=')
        if re.match(regex.VAR_NAME_REGEX, key):
            return key, value
        raise RuntimeError(key_value_str)

    def invoke(self, args=None):
        print(f"Generate.invoke: {args}")
        temgen_instance = temgen.Temgen(make_basic_ui_from_name(args.basic_ui),
                                        var_files=args.var_file if args.var_file else [],
                                        var_dict=args.var if args.var else [],
                                        check_template=args.check_template)
        temgen_instance.find_and_treat_template_file(Path(args.template_path),
                                                     args.template_version,
                                                     output_dir=Path(args.output_dir),
                                                     ui=args.ui)
