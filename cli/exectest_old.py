from argparse import ArgumentParser
import re

# https://mike.depalatis.net/blog/simplifying-argparse


class CliCommandWithSubcommand:
    def __init__(self, *args, **kwargs):
        self.__subcommand_label = self.default_subcommand_label()
        subparsers = kwargs.get("subparsers")
        if subparsers is None:
            assert "subparsers" not in kwargs
            self.__arg_parser: ArgumentParser = ArgumentParser(self.command_label(), **kwargs)
        else:
            del kwargs["subparsers"]
            self.__arg_parser: ArgumentParser = subparsers.add_parser(self.command_label(), help=self.command_label(),
                                                                      **kwargs)

    def arg_parser(self):
        return self.__arg_parser

    def subcommand_label(self):
        return self.__subcommand_label

    def default_subcommand_label(self):
        return f"{self.command_label()}_subcommand"

    def command_label(self):
        name_comps = re.findall('[A-Z][^A-Z]*', self.__class__.__name__)
        return '-'.join([x.lower() for x in name_comps])

    def parse_and_invoke(self, args):
        args = self.__arg_parser.parse_args(args)
        self.invoke(args)

    def invoke(self, args=None):
        if args is None:
            args = self.__arg_parser.parse_args()
        print(f"cli.invoke.args: {args}")
        # print(f"subcommand: {self.subcommand_label()}")
        arg_name = getattr(args, self.subcommand_label())
        print(f"  arg_name:  {arg_name}")
        if arg_name is None:
            self.__arg_parser.print_help()
            exit(0)
        if hasattr(self, arg_name):
            field = getattr(self, arg_name)
            delattr(args, self.subcommand_label())
            print(f"  found -> call {arg_name}.invoke(args)")
            field.invoke(args)
        else:
            print(f"error: Missing field or method '{arg_name}' in class {self.__class__.__name__}.")
            exit(-1)


class Temgencmd(CliCommandWithSubcommand):
    def __init__(self):
        super().__init__()
        subparsers = \
            self.arg_parser().add_subparsers(dest=self.subcommand_label(), required=False,
                                             metavar="command",
                                             help=self.subcommand_label() + " help",
                                             )
        self.generate = self.Generate(subparsers)
        self.config = self.Config(subparsers)

    class Generate(CliCommandWithSubcommand):
        def __init__(self, subparsers):
            super().__init__(subparsers=subparsers)
            self.arg_parser().add_argument("template_file_path", type=str)

        def invoke(self, args=None):
            print(f"Generate.invoke: {args}")

    class Config(CliCommandWithSubcommand):
        def __init__(self, subparsers):
            super().__init__(subparsers=subparsers)
            subparsers = \
                self.arg_parser().add_subparsers(dest=self.subcommand_label(), required=False,
                                                 metavar="command",
                                                 help=self.subcommand_label() + " help",
                                                 )
            self.list = self.List(subparsers)
            self.create = self.Create(subparsers)

        class List(CliCommandWithSubcommand):
            def __init__(self, subparsers):
                super().__init__(subparsers=subparsers)

            def invoke(self, args=None):
                print(f"List.invoke: {args}")

        class Create(CliCommandWithSubcommand):
            def __init__(self, subparsers):
                super().__init__(subparsers=subparsers)
                self.arg_parser().add_argument("config_file_name", type=str)

            def invoke(self, args=None):
                print(f"List.invoke: {args}")


def generate(args):
    print("~" * 40)
    print(f"generate: {args}")
    arg_parser: ArgumentParser = ArgumentParser("temgen-generate")
    arg_parser.add_argument("template_file_path", type=str)
    cmd_args, argv = arg_parser.parse_known_args(args)
    print(cmd_args)
    print(argv)


def config(args):
    print("config")
    print("TODO")


def cache(args):
    print("cache")
    print("TODO")


if __name__ == '__main__':
    arg_parser: ArgumentParser = ArgumentParser("temgen", add_help=False)
    arg_parser.add_argument("command", nargs="?", help="Command to execute.")
    arg_parser.add_argument("args", nargs="...", metavar="...", help="Arguments for command")
    # args = arg_parser.parse_args()
    args, argv = arg_parser.parse_known_args()
    print("-" * 40)
    # print(args)
    # print(argv)
    if args.command:
        match args.command:
            # case "generate":
            #     generate(args.args)
            # case "config":
            #     config(args.args)
            # case "cache":
            #     cache(args.args)
            case "generate" | "config" | "cache":
                temgen = Temgencmd()
                temgen.parse_and_invoke(argv + [args.command] + args.args)
            case _:
                temgen = Temgencmd()
                temgen.parse_and_invoke(argv + ["generate", args.command] + args.args)
            # case _:
            #     cmd_args = [args.command] + args.args
            #     generate(cmd_args)
    else:
        temgen = Temgencmd()
        temgen.parse_and_invoke(argv + args.args)
        # print("-h" * 10)
        # arg_parser.print_help()
