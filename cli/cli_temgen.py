import sys

import constants.names
import temgen
from cli.cache import Cache
from cli.config import Config
from cli.generate import Generate
from cli.remove import Remove
from cli.search import Search
from util.cli_command import CliCommand


class CliTemgen(CliCommand):
    def __init__(self):
        super().__init__(None, command_name=constants.names.LOWER_PROGRAM_NAME,
                         description=f'{constants.names.LOWER_PROGRAM_NAME} {temgen.Temgen.VERSION}')
        self.arg_parser().add_argument('-v', '--version', action='version',
                                       version=f'{self.command_name()} {temgen.Temgen.VERSION}')
        subparsers = self.add_subcommand_subparsers()
        self.generate = Generate(self, subparsers)
        self.config = Config(self, subparsers)
        # self.cache = Cache(self, subparsers)
        # self.search = Search(self, subparsers)
        # self.remove = Remove(self, subparsers)

    def run(self, argv=None):
        if argv is None:
            argv = sys.argv
        print(argv)
        if len(argv) <= 1:
            self.parse_and_invoke(argv[1:])
            return
        command = argv[1]
        if hasattr(self, command):
            self.parse_and_invoke(argv[1:])
            return
        match command:
            case '-h' | '--help' | '-v' | '--version':
                self.parse_and_invoke(argv[1:])
            case _:
                self.parse_and_invoke(["generate"] + argv[1:])


if __name__ == '__main__':
    cli_temgen = CliTemgen()
    cli_temgen.run()
