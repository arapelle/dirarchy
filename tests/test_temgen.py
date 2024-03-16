import io
import random
import sys
import unittest
from pathlib import Path

from ui.terminal_ui import TerminalUi
from temgen import Temgen
from tests.dircmp_test_case import DirCmpTestCase


class TestTemgen(DirCmpTestCase):
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
        sys.stdin = io.StringIO(f"{project_root_dir}\ndata\nAlix\nwhite")
        template_generator = Temgen(TerminalUi())
        template_generator.experimental_treat_template_xml_string(template_string,
                                                                  output_dir=Path(self._output_dirname))
        self._compare_output_and_expected(project_root_dir)

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
        template_generator = Temgen(TerminalUi())
        template_generator.treat_template_xml_string(template_string, output_dir=Path(self._output_dirname))
        self._compare_output_and_expected(project_root_dir)

    def test__treat_template_xml_string__vars_rand_value__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="rand_i">
            <random type="int" min="45" max="100" />
        </var>
        <var name="rand_f">
            <random type="float" min="-4.1" max="12.354" />
        </var>
        <var name="rand_digit">
            <random type="digit" min-len="7" max-len="13" />
        </var>
        <var name="rand_alpha">
             <random type="alpha" min-len="4" max-len="9" />
        </var>
        <var name="rand_lower">
             <random type="lower" min-len="4" max-len="9" />
        </var>
        <var name="rand_upper">
             <random type="upper" min-len="4" max-len="9" />
        </var>
        <var name="rand_alnum">
             <random type="alnum" min-len="15" max-len="26" />
        </var>
        <var name="rand_lower_sisy">
             <random type="lower_sisy" min-len="2" max-len="10" />
        </var>
        <var name="rand_upper_sisy">
             <random type="upper_sisy" min-len="2" max-len="10" />
        </var>
        <var name="rand_snake">
             <random type="snake_case" min-len="2" max-len="10" />
        </var>
        <var name="rand_format_cvqd">
             <random type="format_cvqd" fmt="Cvcvq_cvcvq_cv_dd" />
        </var>
        <var name="rand_chars">
             <random char-set="btcdaeiou" min-len="2" max-len="10" />
        </var>
    </vars>
    <dir path="{output_root_dir}" >
        <file path="data.txt" >
rand_i = {rand_i}
rand_f = {rand_f}
rand_digit = {rand_digit}
rand_alpha = {rand_alpha}
rand_lower = {rand_lower}
rand_upper = {rand_upper}
rand_alnum = {rand_alnum}
rand_lower_sisy = {rand_lower_sisy}
rand_upper_sisy = {rand_upper_sisy}
rand_snake = {rand_snake}
rand_format_cvqd = {rand_format_cvqd}
rand_chars = {rand_chars}
        </file>
    </dir>
</template>
"""
        random.seed(42)
        project_root_dir = "template_xml_string__vars_rand_value"
        sys.stdin = io.StringIO(f"{project_root_dir}")
        template_generator = Temgen(TerminalUi())
        template_generator.experimental_treat_template_xml_string(template_string,
                                                                  output_dir=Path(self._output_dirname))
        self._compare_output_and_expected(project_root_dir)

    def test__treat_template_xml_string__dir_calls_template__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <dir template="input/templates/temdir" template-version="1" />
        <file path="doc/info.txt">Info</file>
    </dir>
</template>
        """
        project_root_dir = "template_xml_string__dir_calls_template"
        sys.stdin = io.StringIO(f"{project_root_dir}\nstuff")
        template_generator = Temgen(TerminalUi())
        template_generator.experimental_treat_template_xml_string(template_string,
                                                                  output_dir=Path(self._output_dirname))
        self._compare_output_and_expected(project_root_dir)

    def test__treat_template_xml_string__file_calls_template__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <file template="input/templates/temfile" template-version="1" />
    </dir>
</template>
        """
        project_root_dir = "template_xml_string__file_calls_template"
        sys.stdin = io.StringIO(f"{project_root_dir}\nstuff\ncard")
        template_generator = Temgen(TerminalUi())
        template_generator.experimental_treat_template_xml_string(template_string,
                                                                  output_dir=Path(self._output_dirname))
        self._compare_output_and_expected(project_root_dir)

    def test__treat_template_xml_string__file_copy__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="fruit" value="Ananas" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="list.txt" copy="input/data/fruits.txt" />
    </dir>
</template>
        """
        project_root_dir = "template_xml_string__file_copy"
        sys.stdin = io.StringIO(f"{project_root_dir}")
        template_generator = Temgen(TerminalUi())
        template_generator.experimental_treat_template_xml_string(template_string,
                                                                  output_dir=Path(self._output_dirname))
        self._compare_output_and_expected(project_root_dir)

    @staticmethod
    def if_valid_cmp_str__template_string():
        return """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="first_if" type="gstr" />
        <var name="second_if" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <if expr="'{first_if}' == 'yes'">
            <file path="first_if_alone.txt">data</file>
        </if>
        <if expr="'{first_if}' == 'yes'">
            <if expr="'{second_if}' == 'yes'">
                <file path="second_if_alone.txt">data</file>
            </if>
        </if>
        <if expr="match(r'[a-z]+', '{second_if}')">
            <file path="expr_match.txt">data</file>
        </if>
        <if expr="'{first_if}' == 'yes' and '{second_if}' == 'yes'">
            <file path="and.txt">data</file>
        </if>
        <if expr="'{first_if}' == 'yes'">
            <then>
                <file path="first_then.txt">data</file>
            </then>
            <else>
                <file path="first_else.txt">data</file>
            </else>
        </if>
        <if expr="'{first_if}' == 'yes'">
            <then>
                <if expr="'{second_if}' == 'yes'">
                    <then>
                        <file path="second_then.txt">data</file>
                    </then>
                    <else>
                        <file path="second_else.txt">data</file>
                    </else>
                </if>
            </then>
        </if>
    </dir>
</template>
        """

    def test__treat_template_xml_string__if_valid_cmp_str_yes_yes__ok(self):
        template_string = self.if_valid_cmp_str__template_string()
        project_root_dir = "template_xml_string__if_valid_cmp_str_yes_yes"
        sys.stdin = io.StringIO(f"{project_root_dir}\nyes\nyes")
        template_generator = Temgen(TerminalUi())
        template_generator.experimental_treat_template_xml_string(template_string,
                                                                  output_dir=Path(self._output_dirname))
        self._compare_output_and_expected(project_root_dir)

    def test__treat_template_xml_string__if_valid_cmp_str_yes_no__ok(self):
        template_string = self.if_valid_cmp_str__template_string()
        project_root_dir = "template_xml_string__if_valid_cmp_str_yes_no"
        sys.stdin = io.StringIO(f"{project_root_dir}\nyes\nno")
        template_generator = Temgen(TerminalUi())
        template_generator.experimental_treat_template_xml_string(template_string,
                                                                  output_dir=Path(self._output_dirname))
        self._compare_output_and_expected(project_root_dir)

    def test__treat_template_xml_string__if_valid_cmp_str_NO_NO__ok(self):
        template_string = self.if_valid_cmp_str__template_string()
        project_root_dir = "template_xml_string__if_valid_cmp_str_NO_NO"
        sys.stdin = io.StringIO(f"{project_root_dir}\nNO\nNO")
        template_generator = Temgen(TerminalUi())
        template_generator.experimental_treat_template_xml_string(template_string,
                                                                  output_dir=Path(self._output_dirname))
        self._compare_output_and_expected(project_root_dir)

    def test__treat_template_xml_string__if_invalid_two_then__exception(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="if_expr" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <if expr="'{if_expr}' == 'yes'">
            <then>
                <file path="then.txt" />
            </then>
            <else>
                <file path="else.txt" />
            </else>
            <then>
                <file path="bad.txt" />
            </then>
        </if>
    </dir>
</template>
        """
        try:
            project_root_dir = "template_xml_string__if_invalid_two_then"
            sys.stdin = io.StringIO(f"{project_root_dir}\nno_matter")
            template_generator = Temgen(TerminalUi())
            template_generator.experimental_treat_template_xml_string(template_string,
                                                                      output_dir=Path(self._output_dirname))
            self.fail()
        except RuntimeError as ex:
            self.assertEqual(str(ex), "Too many 'then' nodes for a 'if' node.")

    def test__treat_template_xml_string__if_invalid_two_else__exception(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-z_]+" />
        <var name="if_expr" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <if expr="'{if_expr}' == 'yes'">
            <then>
                <file path="then.txt" />
            </then>
            <else>
                <file path="else.txt" />
            </else>
            <else>
                <file path="bad.txt" />
            </else>
        </if>
    </dir>
</template>
        """
        try:
            project_root_dir = "template_xml_string__if_invalid_two_else"
            sys.stdin = io.StringIO(f"{project_root_dir}\nno_matter")
            template_generator = Temgen(TerminalUi())
            template_generator.experimental_treat_template_xml_string(template_string,
                                                                      output_dir=Path(self._output_dirname))
            self.fail()
        except RuntimeError as ex:
            self.assertEqual(str(ex), "Too many 'else' nodes for a 'if' node.")

    def test__treat_template_xml_string__if_invalid_missing_then__exception(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-z_]+" />
        <var name="if_expr" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <if expr="'{if_expr}' == 'yes'">
            <else>
                <file path="else.txt" />
            </else>
        </if>
    </dir>
</template>
        """
        try:
            project_root_dir = "template_xml_string__if_invalid_missing_then"
            sys.stdin = io.StringIO(f"{project_root_dir}\nno_matter")
            template_generator = Temgen(TerminalUi())
            template_generator.experimental_treat_template_xml_string(template_string,
                                                                      output_dir=Path(self._output_dirname))
            self.fail()
        except RuntimeError as ex:
            self.assertEqual(str(ex), "A 'else' node is provided for a 'if' node but a 'then' node is missing.")

    def test__treat_template_xml_string__if_invalid_unknown_child__exception(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-z_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <if expr="True">
            <then>
                <file path="then.txt" />
            </then>
            <file path="error.txt" />
        </if>
    </dir>
</template>
        """
        try:
            project_root_dir = "template_xml_string__if_invalid_unknown_child"
            sys.stdin = io.StringIO(f"{project_root_dir}")
            template_generator = Temgen(TerminalUi())
            template_generator.experimental_treat_template_xml_string(template_string,
                                                                      output_dir=Path(self._output_dirname))
            self.fail()
        except RuntimeError as ex:
            self.assertEqual(str(ex), "In 'if', bad child node type: file.")


if __name__ == '__main__':
    unittest.main()
