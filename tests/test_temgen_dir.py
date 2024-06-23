import io
import sys
import unittest
from pathlib import Path

from tests import config
from tests.test_temgen_base import TestTemgenBase
from ui.terminal_ui import TerminalBasicUi
from temgen import Temgen


class TestTemgenDir(TestTemgenBase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._local_sub_dirpath = "temgen/dir"
        super().setUpClass()

    def test__treat_template_xml_string__dir_calls_template__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="templates_dir" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <dir template="{templates_dir}/temdir" template-version="1" />
        <file path="doc/info.txt">Info</file>
    </dir>
</template>
        """
        project_root_dir = "template_xml_string__dir_calls_template"
        templates_dir = config.local_templates_dirpath()
        sys.stdin = io.StringIO(f"{project_root_dir}\n{templates_dir}\nstuff")
        template_generator = Temgen(TerminalBasicUi())
        template_generator.treat_template_xml_string(template_string,
                                                     output_dir=Path(self._output_dirpath))
        self._compare_output_and_expected(project_root_dir)

    def test__local_vars__dir_vars__ok(self):
        # dir, vars -> ok (leaf, root)
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="message" type="gstr" />
        <var name="fruit" type="gstr" value="orange" />
    </vars>
    <dir path="{project_root_dir}">
        <dir path="leaf">
            <vars>
                <var name="message" type="gstr" value="leaf" />
                <var name="fruit" type="gstr" />
            </vars>
            <file path="data.txt">{message}: {fruit}</file>
        </dir>
        <file path="data.txt">{message}: {fruit}</file>
    </dir>
</template>
        """
        project_root_dir = "local_vars__dir_vars"
        input_parameters = ["root"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__local_vars__dir_if_vars__ok(self):
        # dir, if, vars -> ok (leaf, root)
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="message" type="gstr" />
        <var name="fruit" type="gstr" value="orange" />
    </vars>
    <dir path="{project_root_dir}">
        <dir path="leaf">
            <if eval="True">
                <vars>
                    <var name="message" type="gstr" value="leaf" />
                    <var name="fruit" type="gstr" />
                </vars>
                <file path="data.txt">{message}: {fruit}</file>
            </if>
        </dir>
        <file path="data.txt">{message}: {fruit}</file>
    </dir>
</template>
        """
        project_root_dir = "local_vars__dir_if_vars"
        input_parameters = ["root"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__local_vars__dir_if_if_vars__ok(self):
        # dir, if, if, then/else, vars -> ok (leaf, branch, root)
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="message" type="gstr" />
        <var name="fruit" type="gstr" value="orange" />
    </vars>
    <dir path="{project_root_dir}">
        <dir path="branch">
            <if eval="True">
                <vars>
                    <var name="message" type="gstr" value="branch" />
                    <var name="fruit" type="gstr" />
                </vars>
                <dir path="leaf">
                    <if eval="True">
                        <then>
                            <vars>
                                <var name="message" type="gstr" value="leaf" />
                                <var name="fruit" type="gstr" />
                            </vars>
                            <file path="data.txt">{message}: {fruit}</file>
                        </then>
                        <else />
                    </if>
                </dir>
                <file path="data.txt">{message}: {fruit}</file>
            </if>
        </dir>
        <file path="data.txt">{message}: {fruit}</file>
    </dir>
</template>
        """
        project_root_dir = "local_vars__dir_if_if_vars"
        input_parameters = ["root"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__local_vars__dir_match_case_vars__ok(self):
        # dir, match, case, vars -> ok (leaf, root)
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="message" type="gstr" />
        <var name="fruit" type="gstr" value="orange" />
    </vars>
    <dir path="{project_root_dir}">
        <dir path="leaf">
            <match value="a">
                <case value="a">
                    <vars>
                        <var name="message" type="gstr" value="leaf" />
                        <var name="fruit" type="gstr" />
                    </vars>
                    <file path="data.txt">{message}: {fruit}</file>
                </case>
            </match>
        </dir>
        <file path="data.txt">{message}: {fruit}</file>
    </dir>
</template>
        """
        project_root_dir = "local_vars__dir_match_case_vars"
        input_parameters = ["root"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__local_vars__dir_template_if_vars__ok(self):
        # dir, template, if, vars -> ok (leaf, root)
        main_template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="sub_template" type="gstr" />
        <var name="message" type="gstr" />
        <var name="fruit" type="gstr" value="orange" />
    </vars>
    <dir path="{project_root_dir}">
        <if template="{sub_template}" />
        <file path="data.txt">{message}: {fruit}</file>
    </dir>
</template>
        """
        sub_template_filepath = self._make_sub_template_filepath("sub_template")
        sub_template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="message" type="gstr" />
        <var name="fruit" type="gstr" value="orange" />
    </vars>
    <if eval="True">
        <vars>
            <var name="message" type="gstr" value="leaf" />
            <var name="fruit" type="gstr" />
        </vars>
        <file path="leaf/data.txt">{message}: {fruit}</file>
    </if>
</template>
        """
        project_root_dir = "local_vars__dir_template_if_vars"
        input_parameters = [str(sub_template_filepath), "root"]
        self._test__treat_template_xml_string_calling_template__ok(main_template_string,
                                                                   sub_template_filepath,
                                                                   sub_template_string,
                                                                   project_root_dir,
                                                                   input_parameters)

    def test__local_vars__dir_var__ok(self):
        # template, var, ... -> ok
        # dir, var -> ok (leaf, root)
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <var name="message" type="gstr" />
    <var name="fruit" type="gstr" value="orange" />
    <dir path="{project_root_dir}">
        <dir path="leaf">
            <var name="message" type="gstr" value="leaf" />
            <var name="fruit" type="gstr" />
            <file path="data.txt">{message}: {fruit}</file>
        </dir>
        <file path="data.txt">{message}: {fruit}</file>
    </dir>
</template>
        """
        project_root_dir = "local_vars__dir_var"
        input_parameters = ["root"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__local_vars__dir_if_var__ok(self):
        # dir, if, var -> ok (leaf, root)
        template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <var name="message" type="gstr" />
    <var name="fruit" type="gstr" value="orange" />
    <dir path="{project_root_dir}">
        <dir path="leaf">
            <if eval="True">
                <var name="message" type="gstr" value="leaf" />
                <var name="fruit" type="gstr" />
                <file path="data.txt">{message}: {fruit}</file>
            </if>
        </dir>
        <file path="data.txt">{message}: {fruit}</file>
    </dir>
</template>
        """
        project_root_dir = "local_vars__dir_if_var"
        input_parameters = ["root"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__local_vars__dir_if_if_var__ok(self):
        # dir, if, if, then/else, var -> ok (leaf, branch, root)
        template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <var name="message" type="gstr" />
    <var name="fruit" type="gstr" value="orange" />
    <dir path="{project_root_dir}">
        <dir path="branch">
            <if eval="True">
                <var name="message" type="gstr" value="branch" />
                <var name="fruit" type="gstr" />
                <dir path="leaf">
                    <if eval="True">
                        <then>
                            <var name="message" type="gstr" value="leaf" />
                            <var name="fruit" type="gstr" />
                            <file path="data.txt">{message}: {fruit}</file>
                        </then>
                        <else />
                    </if>
                </dir>
                <file path="data.txt">{message}: {fruit}</file>
            </if>
        </dir>
        <file path="data.txt">{message}: {fruit}</file>
    </dir>
</template>
        """
        project_root_dir = "local_vars__dir_if_if_var"
        input_parameters = ["root"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__local_vars__dir_match_case_var__ok(self):
        # dir, match, case, var -> ok (leaf, root)
        template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <var name="message" type="gstr" />
    <var name="fruit" type="gstr" value="orange" />
    <dir path="{project_root_dir}">
        <dir path="leaf">
            <match value="a">
                <case value="a">
                    <var name="message" type="gstr" value="leaf" />
                    <var name="fruit" type="gstr" />
                    <file path="data.txt">{message}: {fruit}</file>
                </case>
            </match>
        </dir>
        <file path="data.txt">{message}: {fruit}</file>
    </dir>
</template>
        """
        project_root_dir = "local_vars__dir_match_case_var"
        input_parameters = ["root"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__local_vars__dir_template_if_var__ok(self):
        # dir, template, if, var -> ok (leaf, root)
        main_template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <var name="sub_template" type="gstr" />
    <var name="message" type="gstr" />
    <var name="fruit" type="gstr" value="orange" />
    <dir path="{project_root_dir}">
        <if template="{sub_template}" />
        <file path="data.txt">{message}: {fruit}</file>
    </dir>
</template>
        """
        sub_template_filepath = self._make_sub_template_filepath("sub_template")
        sub_template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <var name="message" type="gstr" />
    <var name="fruit" type="gstr" value="orange" />
    <if eval="True">
        <var name="message" type="gstr" value="leaf" />
        <var name="fruit" type="gstr" />
        <file path="leaf/data.txt">{message}: {fruit}</file>
    </if>
</template>
        """
        project_root_dir = "local_vars__dir_template_if_var"
        input_parameters = [str(sub_template_filepath), "root"]
        self._test__treat_template_xml_string_calling_template__ok(main_template_string,
                                                                   sub_template_filepath,
                                                                   sub_template_string,
                                                                   project_root_dir,
                                                                   input_parameters)


if __name__ == '__main__':
    unittest.main()
