from util.cli_command import CliCommand


class Cache(CliCommand):
    def __init__(self, parent: CliCommand, subparsers):
        super().__init__(parent, subparsers=subparsers,
                         help="TODO")
        self.arg_parser().add_argument("-v", "--version")
        self.arg_parser().add_argument("template_name")
        self.arg_parser().add_argument("file", nargs="+")

    def invoke(self, args=None):
        print(f"Cache.invoke: {args}")
