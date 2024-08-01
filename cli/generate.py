from util.cli_command import CliCommand


class Generate(CliCommand):
    def __init__(self, parent: CliCommand, subparsers):
        super().__init__(parent, subparsers=subparsers, help="generate help message")
        self.arg_parser().add_argument("-o", "--output")
        self.arg_parser().add_argument("template_file_path")

    def invoke(self, args=None):
        print(f"Generate.invoke: {args}")
