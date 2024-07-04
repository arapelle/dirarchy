import io
import sys
import tempfile
import unittest
from pathlib import Path

from ui.terminal_ui import TerminalBasicUi
from ui.tkinter_ui import TkinterBasicUi
from util.random_string import random_lower_sisy_string
from temgen import Temgen
from tests.test_temgen_base import TestTemgenBase


class TestTemgenConfig(TestTemgenBase):
    @classmethod
    def setUpClass(cls) -> None:
        import os
        cls._expected_root_dirname = f"{os.path.dirname(os.path.abspath(__file__))}/expected"
        cls._local_sub_dirpath = "temgen/config"
        super().setUpClass()

    def test__config__templates_dirs__ok(self):
        config_filepath = Path(f"{tempfile.gettempdir()}/config_{random_lower_sisy_string(8)}.toml")
        with open(config_filepath, "w") as config_file:
            config_contents = """
templates_dirs = [ "/path/to/templates", "/my/templates" ]
"""
            config_file.write(config_contents)
            config_file.flush()
        temgen = Temgen(TerminalBasicUi(), config_path=config_filepath)
        dirpaths = temgen.templates_dirpaths()
        self.assertIn(Path("/path/to/templates"), dirpaths)
        self.assertIn(Path("/my/templates"), dirpaths)
        self.assertGreater(len(dirpaths), 2)
        config_filepath.unlink(missing_ok=True)

    def test__config__missing_check_template__ok(self):
        config_filepath = Path(f"{tempfile.gettempdir()}/config_{random_lower_sisy_string(8)}.toml")
        with open(config_filepath, "w") as config_file:
            config_file.write("")
            config_file.flush()
        temgen = Temgen(TerminalBasicUi(), config_path=config_filepath)
        check_template_activated = temgen.check_template_activated()
        self.assertFalse(check_template_activated)
        config_filepath.unlink(missing_ok=True)

    def test__config__check_template__ok(self):
        config_filepath = Path(f"{tempfile.gettempdir()}/config_{random_lower_sisy_string(8)}.toml")
        with open(config_filepath, "w") as config_file:
            config_contents = """
check_template = true
"""
            config_file.write(config_contents)
            config_file.flush()
        temgen = Temgen(TerminalBasicUi(), config_path=config_filepath)
        check_template_activated = temgen.check_template_activated()
        self.assertTrue(check_template_activated)
        config_filepath.unlink(missing_ok=True)

    def test__config__ui_basic_TERMINAL__ok(self):
        config_filepath = Path(f"{tempfile.gettempdir()}/config_{random_lower_sisy_string(8)}.toml")
        with open(config_filepath, "w") as config_file:
            config_contents = """
[ui]
basic = "TERMINAL"
"""
            config_file.write(config_contents)
            config_file.flush()
        temgen = Temgen(None, config_path=config_filepath)
        self.assertTrue(isinstance(temgen.basic_ui(), TerminalBasicUi))
        config_filepath.unlink(missing_ok=True)

    def test__config__ui_basic_TKINTER__ok(self):
        config_filepath = Path(f"{tempfile.gettempdir()}/config_{random_lower_sisy_string(8)}.toml")
        with open(config_filepath, "w") as config_file:
            config_contents = """
[ui]
basic = "TKINTER"
"""
            config_file.write(config_contents)
            config_file.flush()
        temgen = Temgen(None, config_path=config_filepath)
        self.assertTrue(isinstance(temgen.basic_ui(), TkinterBasicUi))
        config_filepath.unlink(missing_ok=True)

    def test__config__ui_extra__ok(self):
        config_filepath = Path(f"{tempfile.gettempdir()}/config_{random_lower_sisy_string(8)}.toml")
        with open(config_filepath, "w") as config_file:
            config_contents = """
[ui.extra]
myui = "{python} ./input/extra_ui/myui.py {output_file} {input_file}"
"""
            config_file.write(config_contents)
            config_file.flush()
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="message" type="str" value="" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt">
'{message}'
        </file>
    </dir>
</template>
        """
        project_root_dir = "extra_ui__valid_config_cmd"
        sys.stdin = io.StringIO(f"{project_root_dir}\n")
        template_generator = Temgen(TerminalBasicUi(), config_path=config_filepath,
                                    var_dict=[("text", "coucou")])
        template_generator.treat_template_xml_string(template_string,
                                                     output_dir=Path(self._output_dirpath),
                                                     ui="myui")
        self._compare_output_and_expected(project_root_dir)
        config_filepath.unlink(missing_ok=True)

    def test__config__variables__any_template__ok(self):
        config_filepath = Path(f"{tempfile.gettempdir()}/config_{random_lower_sisy_string(8)}.toml")
        with open(config_filepath, "w") as config_file:
            config_contents = """
[variables]
message = "banana"
surprise = "chocolate"
"""
            config_file.write(config_contents)
            config_file.flush()
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="message" type="str" value="" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt">
'{message}'
'{surprise}'
        </file>
    </dir>
</template>
        """
        project_root_dir = "variables__any_template"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters,
                                                  config_path=config_filepath)
        config_filepath.unlink(missing_ok=True)

    def test__config__logging__ok(self):
        log_dir = (Path(tempfile.gettempdir()) / "temgentests").as_posix()
        config_filepath = Path(f"{tempfile.gettempdir()}/config_{random_lower_sisy_string(8)}.toml")
        with open(config_filepath, "w") as config_file:
            config_contents = f"""
[logging.file]
enabled = true
level = "DEBUG"
log_format = "%(levelname)-8s: %(message)s"
date_format = "%Y%m%d %H%M%S"
filename_format = "logfile.log"
dir = "{str(log_dir)}"

[logging.console] 
enabled = true
level = "DEBUG"
log_format = "%(levelname)-8s: %(message)s"
date_format = "%Y%m%d %H%M%S"
"""
            config_file.write(config_contents)
            config_file.flush()
        temgen = Temgen(TerminalBasicUi(), config_path=config_filepath)
        file_config = temgen.config()["logging"]["file"]
        self.assertIsNotNone(file_config)
        self.assertTrue(bool(file_config["enabled"]))
        self.assertEqual(file_config["level"], "DEBUG")
        self.assertEqual(file_config["log_format"], "%(levelname)-8s: %(message)s")
        self.assertEqual(file_config["date_format"], "%Y%m%d %H%M%S")
        self.assertEqual(file_config["filename_format"], "logfile.log")
        self.assertEqual(file_config["dir"], log_dir)
        self.assertEqual(len(file_config), 6)
        console_config = temgen.config()["logging"]["console"]
        self.assertIsNotNone(console_config)
        self.assertTrue(bool(console_config["enabled"]))
        self.assertEqual(console_config["level"], "DEBUG")
        self.assertEqual(console_config["log_format"], "%(levelname)-8s: %(message)s")
        self.assertEqual(console_config["date_format"], "%Y%m%d %H%M%S")
        self.assertEqual(len(console_config), 4)
        config_filepath.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
