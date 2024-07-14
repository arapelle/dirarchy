import argparse

from cli_command import CliCommand

# https://mike.depalatis.net/blog/simplifying-argparse

class Temgen(CliCommand):
    def __init__(self):
        super().__init__(default="alpha-command")
        subparsers = self.arg_parser().add_subparsers(dest=self.subcommand_label(), required=False,
                                                      metavar="command",
                                                      #title=None,
                                                      help=self.subcommand_label() + " help")
        self.alpha_command = AlphaCommand(subparsers)
        self.beta_command = BetaCommand(subparsers)


class AlphaCommand(CliCommand):
    def __init__(self, subparsers):
        super().__init__(subparsers)
        subparsers = self.arg_parser().add_subparsers(dest=self.subcommand_label(), required=True)
        self.red = Red(subparsers)
        self.orange = Orange(subparsers)
        self.yellow = Yellow(subparsers)


class Red(CliCommand):
    def __init__(self, subparsers):
        super().__init__(subparsers)
        subparsers = self.arg_parser().add_subparsers(dest=self.subcommand_label(), required=True)
        self.add_one_parser(subparsers)
        self.add_two_parser(subparsers)

    def add_one_parser(self, subparsers):
        parser: argparse.ArgumentParser = subparsers.add_parser("one")
        parser.add_argument("element")

    def add_two_parser(self, subparsers):
        parser: argparse.ArgumentParser = subparsers.add_parser("two")
        parser.add_argument("element")

    def one(self, args):
        print(args)

    def two(self, args):
        print(args)


class Orange(CliCommand):
    def __init__(self, subparsers):
        super().__init__(subparsers)
        subparsers = self.arg_parser().add_subparsers(dest=self.subcommand_label(), required=True)
        self.add_one_parser(subparsers)
        self.add_two_parser(subparsers)

    def add_one_parser(self, subparsers):
        parser: argparse.ArgumentParser = subparsers.add_parser("one")
        parser.add_argument("element")

    def add_two_parser(self, subparsers):
        parser: argparse.ArgumentParser = subparsers.add_parser("two")
        parser.add_argument("element")

    def one(self, args):
        print(args)

    def two(self, args):
        print(args)


class Yellow(CliCommand):
    def __init__(self, subparsers):
        super().__init__(subparsers)
        self.arg_parser().add_argument("element")

#    def invoke(self, args=None):
#        print(args)


class BetaCommand(CliCommand):
    def __init__(self, subparsers):
        super().__init__(subparsers)
        subparsers = self.arg_parser().add_subparsers(dest=self.subcommand_label(), required=True)
        self.add_big_parser(subparsers)
        self.add_small_parser(subparsers)

    def add_big_parser(self, subparsers):
        parser: argparse.ArgumentParser = subparsers.add_parser("big")
        parser.add_argument("element")

    def add_small_parser(self, subparsers):
        parser: argparse.ArgumentParser = subparsers.add_parser("small")
        parser.add_argument("element")

    def big(self, args):
        print(args)

    def small(self, args):
        print(args)


if __name__ == '__main__':
    cli_temgen = Temgen()
    cli_temgen.invoke()
