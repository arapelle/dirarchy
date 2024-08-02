from pathlib import Path

import os
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
                             help="TODO")

        def invoke(self, args=None):
            # import glob
            config_dirpath = temgen.Temgen.APPLICATION_DIRECTORIES.settings_dirpath() / "config"
            # for item in glob.glob(str(config_dirpath) + "*.toml")
            #     print(item)
            for _, _, files in os.walk(config_dirpath):
                for file in files:
                    file_path = Path(file)
                    if file_path.suffix == ".toml":
                        print(file_path.stem)

    class Create(CliCommand):
        def __init__(self, parent: CliCommand, subparsers):
            super().__init__(parent, subparsers=subparsers,
                             help="TODO")
            self.arg_parser().add_argument("config_file_name")

        def invoke(self, args=None):
            print(f"List.invoke: {args}")
