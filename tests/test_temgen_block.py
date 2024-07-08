import unittest

from tests.test_temgen_base import TestTemgenBase


class TestTemgenBlock(TestTemgenBase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._local_sub_dirpath = "temgen/block"
        super().setUpClass()

    def test__dir_block__valid_children__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <dir path="{project_root_dir}">
        <var name="message" value="pear" />
        <block>
            <var name="message" value="orange" />
            <dir path="subdir">
                <var name="message" value="apple" />
                <file path="subdir.txt">{message}</file>
            </dir>
            <file path="block.txt">{message}</file>
        </block>
        <file path="root.txt">{message}</file>
    </dir>
</template>
        """
        project_root_dir = "dir_block__valid_children"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__dir_block__invalid_child__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <dir path="{project_root_dir}">
        <block>
            <contents />
            <file path="block.txt" />
        </block>
    </dir>
</template>
        """
        project_root_dir = "dir_block__invalid_child"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'block', bad child node type: contents.", str(err))

    @staticmethod
    def dir_block_calls_template__extends_template__main_str():
        return """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" regex="[a-zA-Z0-9_]+" />
    <var name="template_path" />
    <dir path="{project_root_dir}">
        <var name="message" value="pear" />
        <block template="{template_path}">
            <file path="block2.txt">{message}</file>
            <var name="message" value="banana" />
            <file path="block3.txt">{message}</file>
        </block>
        <file path="root.txt">{message}</file>
    </dir>
</template>
        """

    def test__dir_block_calls_template__extends_template_with_valid_children__ok(self):
        main_template_string = self.dir_block_calls_template__extends_template__main_str()
        sub_template_filepath = self._make_sub_template_filepath("subtemplate")
        sub_template_string = """<?xml version="1.0"?>
<template>
    <block>
        <var name="message" value="orange" />
        <dir path="subdir">
            <var name="message" value="apple" />
            <file path="subdir.txt">{message}</file>
        </dir>
        <file path="block.txt">{message}</file>
    </block>
</template>
        """
        project_root_dir = "dir_block_calls_template__extends_template_with_valid_children"
        input_parameters = [str(sub_template_filepath)]
        self._test__treat_template_xml_string_calling_template__ok(main_template_string,
                                                                   sub_template_filepath,
                                                                   sub_template_string,
                                                                   project_root_dir,
                                                                   input_parameters)

    def test__dir_block_calls_template__extends_template_with_invalid_children__ok(self):
        main_template_string = self.dir_block_calls_template__extends_template__main_str()
        sub_template_filepath = self._make_sub_template_filepath("subtemplate")
        sub_template_string = """<?xml version="1.0"?>
<template>
    <block>
        <contents />
    </block>
</template>
        """
        project_root_dir = "dir_block_calls_template__extends_template_with_invalid_children"
        input_parameters = [str(sub_template_filepath)]
        try:
            self._test__treat_template_xml_string_calling_template__ok(main_template_string,
                                                                       sub_template_filepath,
                                                                       sub_template_string,
                                                                       project_root_dir,
                                                                       input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'block', bad child node type: contents.", str(err))

    def test__template_block__valid_children__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <block>
        <dir path="{project_root_dir}">
            <file path="data.txt" />
        </dir>
    </block>
</template>
        """
        project_root_dir = "template_block__valid_children"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__template_block_calls_template__extends_template_with_valid_children__ok(self):
        main_template_string = """<?xml version="1.0"?>
<template>
    <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    <var name="template_path" />
    <block template="{template_path}" />
</template>
        """
        sub_template_filepath = self._make_sub_template_filepath("subtemplate")
        sub_template_string = """<?xml version="1.0"?>
<template>
    <block>
        <dir path="{project_root_dir}">
            <file path="data.txt" />
        </dir>
    </block>
</template>
        """
        project_root_dir = "template_block_calls_template__extends_template_with_valid_children"
        input_parameters = [str(sub_template_filepath)]
        self._test__treat_template_xml_string_calling_template__ok(main_template_string,
                                                                   sub_template_filepath,
                                                                   sub_template_string,
                                                                   project_root_dir,
                                                                   input_parameters)


if __name__ == '__main__':
    unittest.main()
