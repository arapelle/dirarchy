import random
import unittest

from tests.test_temgen_base import TestTemgenBase


class TestTemgenVars(TestTemgenBase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._local_sub_dirpath = "temgen/vars"
        super().setUpClass()

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
        <var name="rand_alpha_fixed_len">
             <random type="alpha" len="6" />
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
rand_alpha_fixed_len = {rand_alpha_fixed_len}
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
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__vars_rand_value_default__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="rand_i">
            <random type="int" max="0" />
        </var>
        <var name="rand_f">
            <random type="float" max="0" />
        </var>
        <var name="rand_alpha">
             <random type="alpha" max-len="0" />
        </var>
    </vars>
    <dir path="{output_root_dir}" >
        <file path="data.txt" >
rand_i = {rand_i}
rand_f = {rand_f}
rand_alpha = '{rand_alpha}'
        </file>
    </dir>
</template>
"""
        random.seed(42)
        project_root_dir = "template_xml_string__vars_rand_value_default"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    @staticmethod
    def vars__template_string(vars_str: str, file_contents: str):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
{vars_str}
    </vars>
    <dir path="{{output_root_dir}}" >
        <file path="data.txt">
{file_contents}
        </file>
    </dir>
</template>
"""

    @staticmethod
    def vars_bool__template_string():
        vars_str = """
        <var name="first" type="bool" />
        <var name="second" type="bool" />
        <var name="third" type="bool" />
        """
        file_contents = "bools = {first}, {second}, {third}"
        return TestTemgenVars.vars__template_string(vars_str, file_contents)

    def test__treat_template_xml_string__vars_bool__y_Y_True__ok(self):
        template_string = self.vars_bool__template_string()
        project_root_dir = "template_xml_string__vars_bool__y_Y_True"
        input_parameters = ["", "false", "no", "y", "Y", "True"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__vars_bool__n_N_False__ok(self):
        template_string = self.vars_bool__template_string()
        project_root_dir = "template_xml_string__vars_bool__n_N_False"
        input_parameters = ["", "true", "yes", "n", "N", "False"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__vars_int__ok(self):
        vars_str = """
        <var name="first" type="int" />
        <var name="second" type="int" />
        """
        file_contents = "ints = {first}, {second}"
        template_string = self.vars__template_string(vars_str, file_contents)
        project_root_dir = "template_xml_string__vars_int"
        input_parameters = ["7t", "42.5", "36", "-42.5", "-37"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__vars_uint__ok(self):
        vars_str = """
        <var name="first" type="uint" />
        """
        file_contents = "uints = {first}"
        template_string = self.vars__template_string(vars_str, file_contents)
        project_root_dir = "template_xml_string__vars_uint"
        input_parameters = ["7t", "42.5", "-42.5", "-37", "36"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__vars_float__ok(self):
        vars_str = """
        <var name="first" type="float" />
        <var name="second" type="float" />
        <var name="third" type="float" />
        <var name="fourth" type="float" />
        <var name="fifth" type="float" />
        <var name="sixth" type="float" />
        """
        file_contents = "floats = {first}, {second}, {third}, {fourth}, {fifth}, {sixth}"
        template_string = self.vars__template_string(vars_str, file_contents)
        project_root_dir = "template_xml_string__vars_float"
        input_parameters = ["7t", "52", "-32", "65.0", "67.2", "-72.0", "-74.3"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__vars_str__ok(self):
        vars_str = """
        <var name="first" type="str" />
        <var name="second" type="str" />
        <var name="third" type="str" />
        <var name="fourth" type="str" />
        """
        file_contents = "strs = '{first}', '{second}', '{third}', '{fourth}'"
        template_string = self.vars__template_string(vars_str, file_contents)
        project_root_dir = "template_xml_string__vars_str"
        input_parameters = ["", "  ", "info", "  info  "]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__vars_pstr__ok(self):
        vars_str = """
        <var name="first" type="pstr" />
        <var name="second" type="pstr" />
        <var name="third" type="pstr" />
        """
        file_contents = "pstrs = '{first}', '{second}', '{third}'"
        template_string = self.vars__template_string(vars_str, file_contents)
        project_root_dir = "template_xml_string__vars_pstr"
        input_parameters = ["", "  ", "info", "  info  "]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__vars_gstr__ok(self):
        vars_str = """
        <var name="first" type="pstr" />
        <var name="second" type="pstr" />
        """
        file_contents = "gstrs = '{first}', '{second}'"
        template_string = self.vars__template_string(vars_str, file_contents)
        project_root_dir = "template_xml_string__vars_gstr"
        input_parameters = ["", "  ", "info", "  info  "]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__vars_bad_type__exception(self):
        var_type = "conaipa"
        vars_str = f"""
        <var name="first" type="{var_type}" />
        """
        file_contents = "any = {first}"
        template_string = self.vars__template_string(vars_str, file_contents)
        project_root_dir = "template_xml_string__vars_gstr"
        input_parameters = ["", "  ", "info", "  info  "]
        try:
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertTrue(str(err).startswith("Bad var_type: '"))
            self.assertTrue(str(err).find(f"{var_type}") != -1)

    def test__treat_template_xml_string__vars_default__ok(self):
        vars_str = """
        <var name="first" type="gstr" default="dummy" />
        """
        file_contents = "str = '{first}'"
        template_string = self.vars__template_string(vars_str, file_contents)
        project_root_dir = "template_xml_string__vars_default"
        input_parameters = ["\n"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__vars_regex__ok(self):
        vars_str = """
        <var name="first" type="gstr" regex="[A-Z]{4}_[0-9]{2}" />
        """
        file_contents = "str = '{first}'"
        template_string = self.vars__template_string(vars_str, file_contents)
        project_root_dir = "template_xml_string__vars_regex"
        input_parameters = ["\n", "bale_26", "BANA23", "AZER_58"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    @staticmethod
    def var_try_override__str(var_attrs: str, var_text):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="message" {var_attrs}>{var_text}</var>
    </vars>
    <dir path="{{output_root_dir}}" >
        <file path="data.txt" >
message = '{{message}}'
        </file>
    </dir>
</template>
"""

    def test__var_value__not_overrided__ok(self):
        template_string = self.var_try_override__str('value="immutable"', "")
        project_root_dir = "var_value__not_overrided"
        input_parameters = []
        variables = {"message": "overrided"}
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters,
                                                  var_dict=variables)

    def test__var_text__not_overrided__ok(self):
        template_string = self.var_try_override__str('',
                                                     "immutable")
        project_root_dir = "var_text__not_overrided"
        input_parameters = []
        variables = {"message": "overrided"}
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters,
                                                  var_dict=variables)

    def test__var_default__overrided__ok(self):
        template_string = self.var_try_override__str('default="default_value" if-unset="use-default"', "")
        project_root_dir = "var_default__overrided"
        input_parameters = []
        variables = {"message": "overrided"}
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters,
                                                  var_dict=variables)

    def test__treat_template_xml_string__vars_if__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="choice" type="gstr" />
        <if eval="'{choice}' == 'even'">
            <then>
                <var name="number" value="86420" />
            </then>
            <else>
                <var name="number" value="97531" />
            </else>
        </if>
    </vars>
    <dir path="{output_root_dir}" >
        <file path="data.txt" >
{number}
        </file>
    </dir>
</template>
"""
        random.seed(42)
        project_root_dir = "template_xml_string__vars_if"
        input_parameters = ["even"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__vars_match__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="choice" type="gstr" />
        <match value="{choice}">
            <case value="normal">
                <var name="value" value="value" />
            </case>
            <case value="super">
                <var name="value" value="super_value" />
            </case>
            <case>
                <var name="value" value="default_value" />
            </case>
        </match>
    </vars>
    <dir path="{output_root_dir}" >
        <file path="data.txt" >
{value}
        </file>
    </dir>
</template>
"""
        random.seed(42)
        project_root_dir = "template_xml_string__vars_match"
        input_parameters = ["super"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__var_from_text__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="text" type="gstr">Hello world</var>
    </vars>
    <dir path="{output_root_dir}">
        <file path="data.txt">
{text}
        </file>
    </dir>
</template>
"""
        project_root_dir = "var_from_text"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__var_from_text_and_value__exception(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="text" type="gstr" value="val">text</var>
    </vars>
    <dir path="{output_root_dir}">
        <file path="data.txt">
{text}
        </file>
    </dir>
</template>
"""
        project_root_dir = "var_from_text_and_value"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual(str(err), "For 'var', you cannot provide value and text at the same time.")

    def test__var_from_file__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="fruit" type="gstr" />
        <var name="text" type="gstr" format="format" strip="strip" copy="input/data/fruits.txt" />
    </vars>
    <dir path="{output_root_dir}">
        <file path="data.txt">
{text}
        </file>
    </dir>
</template>
"""
        project_root_dir = "var_from_file"
        input_parameters = ["Ananas"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__var_from_file_and_text__exception(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="fruit" type="gstr" />
        <var name="text" type="gstr" format="format" strip="strip" copy="input/data/fruits.txt">text</var>
    </vars>
    <dir path="{output_root_dir}">
        <file path="data.txt">
{text}
        </file>
    </dir>
</template>
"""
        project_root_dir = "var_from_file_and_text"
        input_parameters = ["Ananas"]
        try:
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("No text is expected when copying a file.", str(err))

    def test__var_from_contents__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="fruit" type="gstr" />
        <var name="text" type="gstr">
            <contents>
                <contents strip="strip-nl">Fruits:</contents>
                <contents format="format" strip="strip" copy="input/data/fruits.txt" />
            </contents>
        </var>
    </vars>
    <dir path="{output_root_dir}">
        <file path="data.txt">
{text}
        </file>
    </dir>
</template>
"""
        project_root_dir = "var_from_contents"
        input_parameters = ["Ananas"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__var_from_contents_and_value__exception(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="text" type="gstr" value="val"><contents copy="input/data/fruits.txt" /></var>
    </vars>
    <dir path="{output_root_dir}">
        <file path="data.txt">
{text}
        </file>
    </dir>
</template>
"""
        project_root_dir = "var_from_contents_and_value"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("No child statement is expected when using value attribute.", str(err))

    def test__var_if_text__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="choice" type="gstr" />
        <var name="text" type="gstr" strip="strip">
            <if eval="'{choice}' == 'then'">
                <then>
                    THEN
                </then>
                <else>
                    ELSE
                </else>
            </if>
        </var>
    </vars>
    <dir path="{output_root_dir}">
        <file path="data.txt">
'{text}'
        </file>
    </dir>
</template>
"""
        project_root_dir = "var_if_text"
        input_parameters = ["then"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__var_match_text__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="choice" type="gstr" />
        <var name="text" type="gstr" strip="strip">
            <match value="{choice}">
                <case value="one">
                    ONE
                </case>
                <case value="two">
                    TWO
                </case>
                <case>
                    DEFAULT
                </case>
            </match>
        </var>
    </vars>
    <dir path="{output_root_dir}">
        <file path="data.txt">
'{text}'
        </file>
    </dir>
</template>
"""
        project_root_dir = "var_match_text"
        input_parameters = ["two"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__vars_vars__exception(self):
        # vars, vars -> exception
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <vars />
    </vars>
    <file path="{output_root_dir}/data.txt" />
</template>
"""
        project_root_dir = "vars_vars"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'vars', bad child node type: vars.", str(err))

    def test__vars_if_vars__exception(self):
        # vars, if, vars -> exception
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <if eval="True">
            <vars />
        </if>
    </vars>
    <file path="{output_root_dir}/data.txt" />
</template>
"""
        project_root_dir = "vars_if_vars"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'if', bad child node type: vars.", str(err))

    def test__vars_match_case_vars__exception(self):
        # vars, match, case, vars -> exception
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <match value="a">
            <case value="a">
                <vars />
            </case>
        </match>
    </vars>
    <file path="{output_root_dir}/data.txt" />
</template>
"""
        project_root_dir = "vars_match_case_vars"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'case', bad child node type: vars.", str(err))

    def test__var_vars__exception(self):
        # var, vars -> exception
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="arg" type="gstr">
            <vars />
        </var>
    </vars>
    <file path="{output_root_dir}/data.txt" />
</template>
"""
        project_root_dir = "var_vars"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'var', bad child node type: vars.", str(err))

    def test__var_var__exception(self):
        # var, var -> exception
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="arg" type="gstr">
            <var />
        </var>
    </vars>
    <file path="{output_root_dir}/data.txt" />
</template>
"""
        project_root_dir = "var_var"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'var', bad child node type: var.", str(err))

    def test__var_if_vars__exception(self):
        # var, if, vars -> exception
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="arg" type="gstr">
            <if eval="True">
                <vars />
            </if>
        </var>
    </vars>
    <file path="{output_root_dir}/data.txt" />
</template>
"""
        project_root_dir = "var_if_vars"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'if', bad child node type: vars.", str(err))

        def test__var_if_var__exception(self):
            # var, if, var -> exception
            template_string = """<?xml version="1.0"?>
    <template>
        <vars>
            <var name="output_root_dir" type="gstr" />
            <var name="arg" type="gstr">
                <if eval="True">
                    <var />
                </if>
            </var>
        </vars>
        <file path="{output_root_dir}/data.txt" />
    </template>
    """
            project_root_dir = "var_if_var"
            input_parameters = []
            try:
                self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
            except RuntimeError as err:
                self.assertEqual("In 'if', bad child node type: var.", str(err))

    def test__var_match_case_vars__exception(self):
        # var, match, case, vars -> exception
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="arg" type="gstr">
            <match value="a">
                <case value="a">
                    <vars />
                </case>
            </match>
        </var>
    </vars>
    <file path="{output_root_dir}/data.txt" />
</template>
"""
        project_root_dir = "var_match_case_vars"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'case', bad child node type: vars.", str(err))

    def test__var_match_case_var__exception(self):
        # var, match, case, var -> exception
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="output_root_dir" type="gstr" />
        <var name="arg" type="gstr">
            <match value="a">
                <case value="a">
                    <var />
                </case>
            </match>
        </var>
    </vars>
    <file path="{output_root_dir}/data.txt" />
</template>
"""
        project_root_dir = "var_match_case_var"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'case', bad child node type: var.", str(err))

    def test__vars_calls_ui__valid_ui__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <var name="text" value="novel" />
    <var name="message" type="str" value="bad_value" />
    <dir path="{project_root_dir}">
        <vars ui="{python} ./input/extra_ui/myui.py {output_file} {input_file}">
            <var name="message" type="str" />
        </vars>
        <file path="data.txt">
'{message}'
        </file>
    </dir>
</template>
        """
        project_root_dir = "vars_calls_ui__valid_ui"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__vars_calls_ui__valid_ui_no_input__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <dir path="{project_root_dir}">
        <vars ui="{python} ./input/extra_ui/myui_no_input.py {1}">
            <var name="message" />
        </vars>
        <var name="end_message" />
        <file path="data.txt">
'{message}'
'{end_message}'
        </file>
    </dir>
</template>
        """
        project_root_dir = "vars_calls_ui__valid_ui_no_input"
        input_parameters = ["default_end_message"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__vars_calls_ui__empty_ui__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <dir path="{project_root_dir}">
        <vars ui="">
            <var name="message" default="UNSET" if-unset="use-default" />
        </vars>
        <file path="data.txt">
'{message}'
        </file>
    </dir>
</template>
        """
        project_root_dir = "vars_calls_ui__empty_ui"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__vars_calls_ui__not_found_ui__exception(self):
        template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <dir path="{project_root_dir}">
        <vars ui="{python} ./input/extra_ui/unknown.py {1}">
            <var name="message" type="str" />
        </vars>
        <file path="data.txt">
'{message}'
        </file>
    </dir>
</template>
        """
        project_root_dir = "vars_calls_ui__not_found_ui"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertTrue(str(err).find("Execution of ui did not work well") != -1)

    def test__if_unset__use_default_provided__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <var name="vegetable" type="gstr" if-unset="ask" default="carrot" />
    <var name="fruit" type="gstr" if-unset="use-default" default="ananas" />
    <dir path="{project_root_dir}">
        <file path="data.txt">
vegetable='{vegetable}'
fruit='{fruit}'
        </file>
    </dir>
</template>
        """
        project_root_dir = "if_unset__use_default_provided"
        input_parameters = ["potato"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__if_unset__use_default_not_provided__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <var name="bool_val" type="bool" if-unset="use-default" />
    <var name="int_val" type="int" if-unset="use-default" />
    <var name="uint_val" type="uint" if-unset="use-default" />
    <var name="float_val" type="float" if-unset="use-default" />
    <var name="str_val" type="str" if-unset="use-default" />
    <dir path="{project_root_dir}">
        <file path="data.txt">
bool_val='{bool_val}'
int_val='{int_val}'
uint_val='{uint_val}'
float_val='{float_val}'
str_val='{str_val}'
        </file>
    </dir>
</template>
        """
        project_root_dir = "if_unset__use_default_not_provided"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    @staticmethod
    def __if_unset_default_missing_template_str(var_type):
        return f"""<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <var name="str_val" type="{var_type}" if-unset="use-default" />
    <dir path="{{project_root_dir}}">
        <file path="data.txt">
str_val='{{str_val}}'
        </file>
    </dir>
</template>
        """

    def test__if_unset__use_default_missing_pstr__exception(self):
        var_type = "pstr"
        template_string = self.__if_unset_default_missing_template_str(var_type)
        project_root_dir = "if_unset__use_default_missing"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as error:
            self.assertEqual(f"Action 'use-default' is chosen for the unset variable 'str_val of type '{var_type}', "
                             "but the default value is missing (use attribute 'default').", str(error))

    def test__if_unset__use_default_missing_gstr__exception(self):
        var_type = "gstr"
        template_string = self.__if_unset_default_missing_template_str(var_type)
        project_root_dir = "if_unset__use_default_missing"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as error:
            self.assertEqual(f"Action 'use-default' is chosen for the unset variable 'str_val of type '{var_type}', "
                             "but the default value is missing (use attribute 'default').", str(error))

    @staticmethod
    def dir_template_twice_vars__str():
        return """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <vars>
        <var name="fruit" type="str" value="orange" />
    </vars>
    <var name="color" type="str" value="red" />
    <dir path="{project_root_dir}">
        <file path="data.txt">
fruit='{fruit}'
color='{color}'
        </file>
    </dir>
</template>
        """

    def test__template_twice_vars__ok(self):
        template_string = self.dir_template_twice_vars__str()
        project_root_dir = "template_twice_vars"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__dir_calls_template_twice_vars__ok(self):
        main_template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <var name="template_path" type="str" />
    <dir template="{template_path}" />
</template>
        """
        sub_template_filepath = self._make_sub_template_filepath("sub_template")
        sub_template_string = self.dir_template_twice_vars__str()
        project_root_dir = "dir_calls_template_twice_vars"
        input_parameters = [str(sub_template_filepath)]
        self._test__treat_template_xml_string_calling_template__ok(main_template_string,
                                                                   sub_template_filepath,
                                                                   sub_template_string,
                                                                   project_root_dir,
                                                                   input_parameters)

    def test__vars_calls_template__ok(self):
        sub_template_filepath = self._make_sub_template_filepath("sub_template")
        main_template_string = f"""<?xml version="1.0"?>
<template>
    <vars template="{str(sub_template_filepath)}">
        <var name="color" type="str" value="red" />
    </vars>
    <dir path="{{project_root_dir}}">
        <file path="data.txt">
fruit='{{fruit}}'
color='{{color}}'
        </file>
    </dir>
</template>
        """
        sub_template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="fruit" type="str" value="orange" />
    </vars>
</template>
        """
        project_root_dir = "vars_calls_template"
        input_parameters = []
        self._test__treat_template_xml_string_calling_template__ok(main_template_string,
                                                                   sub_template_filepath,
                                                                   sub_template_string,
                                                                   project_root_dir,
                                                                   input_parameters)

    def test__vars_calls_template_twice_vars__exception(self):
        sub_template_filepath = self._make_sub_template_filepath("sub_template")
        main_template_string = f"""<?xml version="1.0"?>
<template>
    <vars template="{str(sub_template_filepath)}" />
    <dir path="{{project_root_dir}}" />
</template>
        """
        sub_template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <vars>
        <var name="fruit" type="str" value="orange" />
    </vars>
</template>
        """
        project_root_dir = "vars_calls_template_twice_vars"
        input_parameters = []
        try:
            self._test__treat_template_xml_string_calling_template__exception(main_template_string,
                                                                              sub_template_filepath,
                                                                              sub_template_string,
                                                                              project_root_dir,
                                                                              input_parameters)
        except RuntimeError as err:
            self.assertEqual("Too many nodes under <template>.", str(err))

    def test__vars_calls_template_vars_var__exception(self):
        sub_template_filepath = self._make_sub_template_filepath("sub_template")
        main_template_string = f"""<?xml version="1.0"?>
<template>
    <vars template="{str(sub_template_filepath)}" />
    <dir path="{{project_root_dir}}" />
</template>
        """
        sub_template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <var name="fruit" type="str" value="orange" />
</template>
        """
        project_root_dir = "vars_calls_template_vars_var"
        input_parameters = []
        try:
            self._test__treat_template_xml_string_calling_template__exception(main_template_string,
                                                                              sub_template_filepath,
                                                                              sub_template_string,
                                                                              project_root_dir,
                                                                              input_parameters)
        except RuntimeError as err:
            self.assertEqual("Too many nodes under <template>.", str(err))

    def test__vars_calls_template_var__exception(self):
        sub_template_filepath = self._make_sub_template_filepath("sub_template")
        main_template_string = f"""<?xml version="1.0"?>
<template>
    <vars template="{str(sub_template_filepath)}" />
    <dir path="{{project_root_dir}}" />
</template>
        """
        sub_template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
</template>
        """
        project_root_dir = "vars_calls_template_var"
        input_parameters = []
        try:
            self._test__treat_template_xml_string_calling_template__exception(main_template_string,
                                                                              sub_template_filepath,
                                                                              sub_template_string,
                                                                              project_root_dir,
                                                                              input_parameters)
        except RuntimeError as err:
            self.assertEqual("Unexpected node (var) under <template>. Expected: vars.", str(err))

    def test__var__set_twice__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="color" value="green" />
        <var name="color" value="orange" />
        <var name="color" value="light_{color}" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt">
color = '{color}'
        </file>
    </dir>
</template>
        """
        project_root_dir = "var__set_twice"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__var__value_with_escape_chars__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="message" value="begin\\nend" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt">
message = '{message}'
        </file>
    </dir>
</template>
        """
        project_root_dir = "var__value_with_escape_chars"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)


if __name__ == '__main__':
    unittest.main()
