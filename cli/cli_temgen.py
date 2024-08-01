import sys

import temgen
from cli.cache import Cache
from cli.config import Config
from cli.generate import Generate
from cli.remove import Remove
from cli.search import Search
from util.cli_command import CliCommand


class CliTemgen(CliCommand):
    def __init__(self):
        super().__init__(None, command_name="temgen")
        self.arg_parser().add_argument('-v', '--version', action='version',
                                       version=f'{self.command_name()} {temgen.Temgen.VERSION}')
        subparsers = self.add_subcommand_subparsers()
        self.generate = Generate(self, subparsers)
        self.config = Config(self, subparsers)
        self.cache = Cache(self, subparsers)
        self.search = Search(self, subparsers)
        self.remove = Remove(self, subparsers)


if __name__ == '__main__':
    cli_temgen = CliTemgen()
    program_args = sys.argv
    print(program_args)
    if len(program_args) <= 1:
        cli_temgen.parse_and_invoke(program_args[1:])
    else:
        command = program_args[1]
        if hasattr(cli_temgen, command):
            cli_temgen.parse_and_invoke(program_args[1:])
        else:
            match command:
                case '-h' | '--help' | '-v' | '--version':
                    cli_temgen.parse_and_invoke(program_args[1:])
                case _:
                    cli_temgen.parse_and_invoke(["generate"] + program_args[1:])
