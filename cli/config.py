from pathlib import Path

import temgen
from util.cli_command import CliCommand


class Config(CliCommand):
    def __init__(self, parent: CliCommand, subparsers):
        super().__init__(parent, subparsers=subparsers,
                         help="Manage the temgen configuration in the temgen home.")
        subparsers = self.add_subcommand_subparsers()
        self.list = self.List(self, subparsers)
        self.create = self.Create(self, subparsers)

    class List(CliCommand):
        def __init__(self, parent: CliCommand, subparsers):
            super().__init__(parent, subparsers=subparsers,
                             help="List the available configurations.")
            argparser = self.arg_parser()
            argparser.add_argument('-f', '--full-path', action='store_true',
                                   dest='full_path', help='Print full paths (absolute).')

        def invoke(self, args=None):
            import glob
            config_dirpath = temgen.Temgen.APPLICATION_DIRECTORIES.settings_dirpath() / "config"
            config_files = glob.glob(f"{config_dirpath}/*.toml")
            for config_file in config_files:
                config_file = Path(config_file)
                if args.full_path:
                    absolute_file_path = config_file.absolute()
                    print(absolute_file_path)
                else:
                    print(config_file.stem)

    class Create(CliCommand):
        def __init__(self, parent: CliCommand, subparsers):
            super().__init__(parent, subparsers=subparsers,
                             help="TODO")
            self.arg_parser().add_argument("config_file_name")

        def invoke(self, args=None):
            print(f"Create.invoke: {args}")
