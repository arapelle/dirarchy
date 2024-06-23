import unittest

from tests.test_temgen_base import TestTemgenBase


class TestTemgenMatch(TestTemgenBase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._local_sub_dirpath = "temgen/match"
        super().setUpClass()

    @staticmethod
    def match__template_string(default_case, no_match_file, cases=None):
        if cases is None:
            cases = """
            <case value="value">
                <file path="value.md" />
            </case>
            <case expr="[a-z]+">
                <file path="expr_az.md" />
            </case>
            <case expr="[0-9]+">
                <file path="expr_09.md" />
            </case>
            """
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-z09_]+" />
        <var name="expr" type="gstr" />
    </vars>
    <dir path="{{project_root_dir}}">
        <match expr="{{expr}}">
            {cases}
            {default_case}
        </match>
        {no_match_file}
    </dir>
</template>
        """

    @staticmethod
    def match_valid__template_string(with_default: bool):
        default_case = ""
        no_match_file = ""
        if with_default:
            default_case = """
            <case>
                <file path="default.md" />
            </case>
            """
        else:
            no_match_file = """
            <file path="no_match.md" />
            """
        return TestTemgenMatch.match__template_string(default_case, no_match_file)

    @staticmethod
    def match_invalid_two_default__template_string():
        default_case = """
        <case>
            <file path="default.md" />
        </case>
        """
        return TestTemgenMatch.match__template_string(default_case, "", default_case)

    @staticmethod
    def match_invalid_missing_case__template_string():
        return TestTemgenMatch.match__template_string("", "", "")

    def test__treat_template_xml_string__match_valid_value__ok(self):
        template_string = self.match_valid__template_string(with_default=True)
        project_root_dir = "template_xml_string__match_valid_value"
        input_parameters = ["value"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__match_valid_expr_09__ok(self):
        template_string = self.match_valid__template_string(with_default=True)
        project_root_dir = "template_xml_string__match_valid_expr_09"
        input_parameters = ["123"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__match_valid_default__ok(self):
        template_string = self.match_valid__template_string(with_default=True)
        project_root_dir = "template_xml_string__match_valid_default"
        input_parameters = ["az09"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__match_valid_no_match__ok(self):
        template_string = self.match_valid__template_string(with_default=False)
        project_root_dir = "template_xml_string__match_valid_no_match"
        input_parameters = ["az09"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__treat_template_xml_string__match_invalid_two_default__exception(self):
        try:
            template_string = self.match_invalid_two_default__template_string()
            project_root_dir = "template_xml_string__match_invalid_two_default"
            input_parameters = ["no_matter"]
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as ex:
            self.assertEqual(str(ex), "A match node cannot have two default case nodes.")

    def test__treat_template_xml_string__match_invalid_missing_case__exception(self):
        try:
            template_string = self.match_invalid_missing_case__template_string()
            project_root_dir = "template_xml_string__match_invalid_missing_case"
            input_parameters = ["no_matter"]
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as ex:
            self.assertEqual(str(ex), "case nodes are missing in match node.")

    def test__expr_cond__using_path__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <match eval="Path('.').resolve()"> 
            <case eval="Path.cwd().resolve()">
                <file path="path_matches.txt" />
            </case>
        </match>
    </dir>
</template>
        """
        project_root_dir = "expr_cond__using_path"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__match_as_tree_root__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="choice" type="gstr" />
    </vars>
    <match expr="{choice}">
        <case value="yes">
            <dir path="{project_root_dir}">
                <file path="data.txt">yes</file>
            </dir>
        </case>
        <case value="no">
            <dir path="{project_root_dir}">
                <file path="data.txt">no</file>
            </dir>
        </case>
    </match>
</template>
        """
        project_root_dir = "match_as_tree_root"
        input_parameters = ["no"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    @staticmethod
    def __match_calls_template__main_template_str(match_attrs="", match_children=""):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="template_path" type="gstr" />
    </vars>
    <dir path="{{project_root_dir}}">
        <match template="{{template_path}}" {match_attrs}>
            {match_children}
        </match>
    </dir>
</template>
        """

    @staticmethod
    def __match_calls_template__sub_template_str():
        return """<?xml version="1.0"?>
<template>
    <vars>
        <var name="choice" type="gstr" />
    </vars>
    <match expr="{choice}">
        <case value="yes">
            <file path="data.txt">yes</file>
        </case>
        <case value="no">
            <file path="data.txt">no</file>
        </case>
    </match>
</template>
        """

    def test__match_calls_template__ok(self):
        main_template_string = self.__match_calls_template__main_template_str()
        sub_template_filepath = self._make_sub_template_filepath("match_file_template")
        sub_template_string = self.__match_calls_template__sub_template_str()
        project_root_dir = "match_calls_template"
        input_parameters = [str(sub_template_filepath), "yes"]
        self._test__treat_template_xml_string_calling_template__ok(main_template_string,
                                                                   sub_template_filepath,
                                                                   sub_template_string,
                                                                   project_root_dir,
                                                                   input_parameters)

    def test__match_calls_template__expr_attr__exception(self):
        main_template_string = self.__match_calls_template__main_template_str('expr="True"')
        sub_template_filepath = self._make_sub_template_filepath("match_file_template")
        sub_template_string = self.__match_calls_template__sub_template_str()
        project_root_dir = "match_calls_template"
        input_parameters = [str(sub_template_filepath), "yes"]
        try:
            self._test__treat_template_xml_string_calling_template__exception(main_template_string,
                                                                              sub_template_filepath,
                                                                              sub_template_string,
                                                                              project_root_dir,
                                                                              input_parameters)
        except RuntimeError as err:
            self.assertEqual("The attribute 'expr' is unexpected when calling a 'match' template.", str(err))

    def test__match_calls_template__child_statement__exception(self):
        match_children = '<case><dir path="bad" /></case>'
        main_template_string = self.__match_calls_template__main_template_str(match_children=match_children)
        sub_template_filepath = self._make_sub_template_filepath("match_file_template")
        sub_template_string = self.__match_calls_template__sub_template_str()
        project_root_dir = "match_calls_template"
        input_parameters = [str(sub_template_filepath), "yes"]
        try:
            self._test__treat_template_xml_string_calling_template__exception(main_template_string,
                                                                              sub_template_filepath,
                                                                              sub_template_string,
                                                                              project_root_dir,
                                                                              input_parameters)
        except RuntimeError as err:
            self.assertEqual("No child statement is expected when calling a 'match' template.", str(err))

    def test__local_vars__match_vars__ok(self):
        # template, match, vars -> ok (leaf)
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="message" type="gstr" />
        <var name="fruit" type="gstr" value="orange" />
    </vars>
    <match value="a">
        <case value="a">
            <vars>
                <var name="message" type="gstr" value="leaf" />
                <var name="fruit" type="gstr" />
            </vars>
            <file path="{project_root_dir}/leaf/data.txt">{message}: {fruit}</file>
        </case>
    </match>
</template>
        """
        project_root_dir = "local_vars__match_vars"
        input_parameters = ["root"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__local_vars__match_var__ok(self):
        # template, match, var -> ok (leaf)
        template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <var name="message" type="gstr" />
    <var name="fruit" type="gstr" value="orange" />
    <match value="a">
        <case value="a">
            <var name="message" type="gstr" value="leaf" />
            <var name="fruit" type="gstr" />
            <file path="{project_root_dir}/leaf/data.txt">{message}: {fruit}</file>
        </case>
    </match>
</template>
        """
        project_root_dir = "local_vars__match_var"
        input_parameters = ["root"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)


if __name__ == '__main__':
    unittest.main()
