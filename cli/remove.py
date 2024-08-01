from util.cli_command import CliCommand


class Remove(CliCommand):
    def __init__(self, parent: CliCommand, subparsers):
        super().__init__(parent, subparsers=subparsers)
        self.arg_parser().add_argument("template_id", metavar="template_name[/version]")

    def invoke(self, args=None):
        print(f"Remove.invoke: {args}")
