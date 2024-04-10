import datetime
import os
import unittest

from statement.template_statement import TemplateStatement
from tests.test_temgen_base import TestTemgenBase


class TestTemgenBasic(TestTemgenBase):
    @classmethod
    def setUpClass(cls) -> None:
        import os
        cls._expected_root_dirname = f"{os.path.dirname(os.path.abspath(__file__))}/expected"
        cls._local_sub_dirpath = "temgen/basic"
        super().setUpClass()

    def test__treat_template_xml_string__bad_root_statement_name__exception(self):
        try:
            template_string = """<?xml version="1.0"?>
<bad_name>
    <dir path="bad_dirtree">
        <file path="data.txt" />
    </dir>
</bad_name>
            """
            project_root_dir = "template_xml_string__bad_root_statement_name"
            input_parameters = []
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual(str(err), f"Root node must be '{TemplateStatement.STATEMENT_LABEL}'!")

    def test__treat_template_xml_string__vars_dir_file__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="file_name" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="name" type="gstr" regex="[A-Z][a-z_]*" />
        <var name="color" type="gstr" regex="[a-z]+" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="{file_name}.txt">
{{ 
    name = {name}, 
    color = {color}
}}
        </file>
    </dir>
</template>
        """
        project_root_dir = "template_xml_string__vars_dir_file"
        input_parameters = ["data", "Alix", "white"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__bad_format_str__exception(self):
        try:
            template_string = """<?xml version="1.0"?>
<template>
    <dir path="{whut" />
</template>
            """
            project_root_dir = "template_xml_string__bad_root_statement_name"
            input_parameters = []
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except ValueError as err:
            self.assertEqual(str(err), "expected '}' before end of string")

    def test__treat_template_xml_string__unknown_var__exception(self):
        try:
            template_string = """<?xml version="1.0"?>
<template>
    <dir path="{unknown_var}" />
</template>
            """
            project_root_dir = "template_xml_string__bad_root_statement_name"
            input_parameters = []
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except KeyError:
            pass

    def test__treat_template_xml_string__builtin_vars__ok(self):
        template_string = """
$TEMPLATE_DIR = "{$TEMPLATE_DIR}"
$YEAR = {$YEAR}
$MONTH = {$MONTH}
$DAY = {$DAY}
$DATE = {$DATE}
$DATE:- = {$DATE:-}
$DATE:_ = {$DATE:_}
$DATE:/ = {$DATE:/}
$TIME = {$TIME}
$TIME:: = {$TIME::}
$STRFTIME = {$STRFTIME:%Y%m%d_%H%M%S}
$ENV:PATH = {$ENV:PATH}
        """.strip()
        project_root_dir = "template_xml_string__builtin_vars"
        input_parameters = []
        output_file_contents = self._run__treat_template_xml_string__file_contents__ok(template_string,
                                                                                       project_root_dir,
                                                                                       input_parameters)
        expected_file_contents = f"""
$TEMPLATE_DIR = ""
$YEAR = %Y
$MONTH = %m
$DAY = %d
$DATE = %Y%m%d
$DATE:- = %Y-%m-%d
$DATE:_ = %Y_%m_%d
$DATE:/ = %Y/%m/%d
$TIME = %H%M%S
$TIME:: = %H:%M:%S
$STRFTIME = %Y%m%d_%H%M%S
$ENV:PATH = {os.environ["PATH"]}
        """
        expected_file_contents = datetime.datetime.now().strftime(expected_file_contents).strip()
        self.assertEqual(output_file_contents, expected_file_contents)


if __name__ == '__main__':
    unittest.main()
