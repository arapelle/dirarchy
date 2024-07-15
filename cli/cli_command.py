import re
from argparse import ArgumentParser


class CliCommand:
    def __init__(self, subparsers=None, arg_name=None, default=None):
        self.__subcommand_label = arg_name if arg_name else self.default_subcommand_label()
        self.__default = default
        if subparsers is None:
            self.__arg_parser: ArgumentParser = ArgumentParser(self.command_label()
                                                               , argument_default=f"%{default}%"
                                                               )
        else:
            self.__arg_parser: ArgumentParser = subparsers.add_parser(self.command_label(), help=self.command_label(),
                                                                      argument_default={
                                                                          "temgen_subcommand": default})

    def arg_parser(self):
        return self.__arg_parser

    def subcommand_label(self):
        return self.__subcommand_label

    def default_subcommand_label(self):
        return f"{self.command_label()}_subcommand"

    def command_label(self):
        name_comps = re.findall('[A-Z][^A-Z]*', self.__class__.__name__)
        return '-'.join([x.lower() for x in name_comps])

    def invoke(self, args=None):
        if args is None:
            args = self.__arg_parser.parse_args()
        print(f"invoke.args: {args}")
        print(f"invoke.arg: {args.toto}")
        print(f"invoke.arg: {args.temgen_subcommand}")
        print(f"subcommand: {self.subcommand_label()}")
        arg_name = getattr(args, self.subcommand_label())
        if arg_name is None:
            use_default = True
            arg_name = self.__default
        print(f"  arg_name:  {arg_name}")
        # assert arg_name is not None
        print(f"  arg_name_: {arg_name}")
        if hasattr(self.__class__, arg_name):
            method = getattr(self.__class__, arg_name)
            delattr(args, self.subcommand_label())
            print(f"  method found -> call self.{arg_name}(args)")
            method(self, args)
        elif hasattr(self, arg_name):
            field = getattr(self, arg_name)
            delattr(args, self.subcommand_label())
            print(f"  attr found -> call {arg_name}.invoke(args)")
            field.invoke(args)
        else:
            print(f"error: Missing field or method '{arg_name}' in class {self.__class__.__name__}.")
            exit(-1)