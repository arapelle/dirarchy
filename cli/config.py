from util.cli_command import CliCommand


class Config(CliCommand):
    def __init__(self, parent: CliCommand, subparsers):
        super().__init__(parent, subparsers=subparsers)
        subparsers = self.add_subcommand_subparsers()
        self.list = self.List(self, subparsers)
        self.create = self.Create(self, subparsers)

    class List(CliCommand):
        def __init__(self, parent: CliCommand, subparsers):
            super().__init__(parent, subparsers=subparsers)

        def invoke(self, args=None):
            print(f"List.invoke: {args}")

    class Create(CliCommand):
        def __init__(self, parent: CliCommand, subparsers):
            super().__init__(parent, subparsers=subparsers)
            self.arg_parser().add_argument("config_file_name")

        def invoke(self, args=None):
            print(f"List.invoke: {args}")
