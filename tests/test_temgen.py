import io
import sys
import unittest
from pathlib import Path

from ui.terminal_ui import TerminalUi
from temgen import Temgen
from tests.dircmp_test_case import DirCmpTestCase


class TestTemgen(DirCmpTestCase):
    def test__treat_template_xml_string__basic_template__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="file_name" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="name" type="gstr" regex="[A-Z][a-z_]*" />
        <var name="color" type="gstr" regex="[a-z]+" />
        <var name="debug" type="bool" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="{file_name}.txt">
{{ 
    name = {name}, 
    color = {color}
}}
        </file>
        <if expr="{debug}">
            <file path="timestamp.txt">
2024-12-06
            </file>
        </if>
    </dir>
</template>
        """
        project_root_dir = "template_xml_string__basic_template"
        sys.stdin = io.StringIO(f"{project_root_dir}\ndata\nAlix\nwhite\ny")
        Temgen.treat_template_xml_string(template_string, ui=TerminalUi(), output_dir=Path(self._output_dirname))
        self._compare_output_and_expected(project_root_dir)


if __name__ == '__main__':
    unittest.main()
