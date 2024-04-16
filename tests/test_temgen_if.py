import unittest

from tests.test_temgen_base import TestTemgenBase


class TestTemgenIf(TestTemgenBase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._local_sub_dirpath = "temgen/if"
        super().setUpClass()

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
        input_parameters = ["yes", "yes"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__if_valid_cmp_str_yes_no__ok(self):
        template_string = self.if_valid_cmp_str__template_string()
        project_root_dir = "template_xml_string__if_valid_cmp_str_yes_no"
        input_parameters = ["yes", "no"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__if_valid_cmp_str_NO_NO__ok(self):
        template_string = self.if_valid_cmp_str__template_string()
        project_root_dir = "template_xml_string__if_valid_cmp_str_NO_NO"
        input_parameters = ["NO", "NO"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__if_valid_cmp_int_6_7__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="first_if" type="int" />
        <var name="second_if" type="int" />
    </vars>
    <dir path="{project_root_dir}">
        <if expr="{first_if} == 6">
            <file path="first_if_alone.txt">data</file>
        </if>
        <if expr="{first_if} == 6">
            <if expr="{second_if} == 7">
                <file path="second_if_alone.txt">data</file>
            </if>
        </if>
        <if expr="match(r'[13579]+', '{second_if}')">
            <file path="expr_match.txt">data</file>
        </if>
        <if expr="{first_if} == 6 and {second_if} == 7">
            <file path="and.txt">data</file>
        </if>
        <if expr="{first_if} == 6">
            <then>
                <file path="first_then.txt">data</file>
            </then>
            <else>
                <file path="first_else.txt">data</file>
            </else>
        </if>
        <if expr="{first_if} == 6">
            <then>
                <if expr="{second_if} == 7">
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
        project_root_dir = "template_xml_string__if_valid_cmp_int_6_7"
        input_parameters = ["6", "7"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

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
            input_parameters = ["no_matter"]
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
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
            input_parameters = ["no_matter"]
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
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
            input_parameters = ["no_matter"]
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
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
            input_parameters = ["no_matter"]
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as ex:
            self.assertEqual(str(ex), "In 'if', bad child node type: file.")

    def test__if_as_tree_root__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="choice" type="gstr" />
    </vars>
    <if expr="'{choice}' == 'yes'">
        <dir path="{project_root_dir}">
            <file path="data.txt">data</file>
        </dir>
    </if>
</template>
        """
        project_root_dir = "if_as_tree_root"
        input_parameters = ["yes"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    @staticmethod
    def __if_calls_template__main_template_str(if_attrs="", if_children=""):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="template_path" type="gstr" />
    </vars>
    <dir path="{{project_root_dir}}">
        <if template="{{template_path}}" {if_attrs}>
            {if_children}
        </if>
    </dir>
</template>
        """

    @staticmethod
    def __if_calls_template__sub_template_str():
        return """<?xml version="1.0"?>
<template>
    <vars>
        <var name="choice" type="gstr" />
    </vars>
    <if expr="'{choice}' == 'yes'">
        <file path="data.txt">data</file>
    </if>
</template>
        """

    def test__if_calls_template__ok(self):
        main_template_string = self.__if_calls_template__main_template_str()
        sub_template_filepath = self._make_sub_template_filepath("if_file_template")
        sub_template_string = self.__if_calls_template__sub_template_str()
        project_root_dir = "if_calls_template"
        input_parameters = [str(sub_template_filepath), "yes"]
        self._test__treat_template_xml_string_calling_template__ok(main_template_string,
                                                                   sub_template_filepath,
                                                                   sub_template_string,
                                                                   project_root_dir,
                                                                   input_parameters)

    def test__if_calls_template__expr_attr__exception(self):
        main_template_string = self.__if_calls_template__main_template_str('expr="True"')
        sub_template_filepath = self._make_sub_template_filepath("if_file_template")
        sub_template_string = self.__if_calls_template__sub_template_str()
        project_root_dir = "if_calls_template"
        input_parameters = [str(sub_template_filepath), "yes"]
        try:
            self._test__treat_template_xml_string_calling_template__exception(main_template_string,
                                                                              sub_template_filepath,
                                                                              sub_template_string,
                                                                              project_root_dir,
                                                                              input_parameters)
        except RuntimeError as err:
            self.assertEqual("The attribute 'expr' is unexpected when calling a 'if' template.", str(err))

    def test__if_calls_template__child_statement__exception(self):
        main_template_string = self.__if_calls_template__main_template_str(if_children='<dir path="bad" />')
        sub_template_filepath = self._make_sub_template_filepath("if_file_template")
        sub_template_string = self.__if_calls_template__sub_template_str()
        project_root_dir = "if_calls_template"
        input_parameters = [str(sub_template_filepath), "yes"]
        try:
            self._test__treat_template_xml_string_calling_template__exception(main_template_string,
                                                                              sub_template_filepath,
                                                                              sub_template_string,
                                                                              project_root_dir,
                                                                              input_parameters)
        except RuntimeError as err:
            self.assertEqual("No child statement is expected when calling a 'if' template.", str(err))


if __name__ == '__main__':
    unittest.main()
