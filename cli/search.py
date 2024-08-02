from util.cli_command import CliCommand


class Search(CliCommand):
    def __init__(self, parent: CliCommand, subparsers):
        super().__init__(parent, subparsers=subparsers,
                         help="TODO")
        self.arg_parser().add_argument("-c", "--cache", action="store_true")
        self.arg_parser().add_argument("-r", "--remote")
        self.arg_parser().add_argument("template_id", metavar="template_name[/version]")

    def invoke(self, args=None):
        print(f"Search.invoke: {args}")
