import datetime
import os
import unittest
from pathlib import Path

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

    @staticmethod
    def __builtin_fsys_vars__vars_list_str(current_working_dir, root_template_dir, template_dir, root_output_dir,
                                           local_root_output_dir, tree_root_output_dir, local_tree_root_output_dir,
                                           output_dir, output_file, output_file_name, output_file_ext,
                                           output_file_exts):
        return f"""
$CURRENT_WORKING_DIR = '{current_working_dir}'
$ROOT_TEMPLATE_DIR = '{root_template_dir}'
$TEMPLATE_DIR = '{template_dir}'
$ROOT_OUTPUT_DIR = '{root_output_dir}'
$LOCAL_ROOT_OUTPUT_DIR = '{local_root_output_dir}'
$TREE_ROOT_OUTPUT_DIR = '{tree_root_output_dir}'
$LOCAL_TREE_ROOT_OUTPUT_DIR = '{local_tree_root_output_dir}'
$OUTPUT_DIR = '{output_dir}'
$OUTPUT_FILE = '{output_file}'
$OUTPUT_FILE_NAME = '{output_file_name}'
$OUTPUT_FILE_EXT = '{output_file_ext}'
$OUTPUT_FILE_EXTS = '{output_file_exts}'
        """

    def __builtin_fsys_vars__template_vars_list_str(self):
        return self.__builtin_fsys_vars__vars_list_str("{$CURRENT_WORKING_DIR}",
                                                       "{$ROOT_TEMPLATE_DIR}",
                                                       "{$TEMPLATE_DIR}",
                                                       "{$ROOT_OUTPUT_DIR}",
                                                       "{$LOCAL_ROOT_OUTPUT_DIR}",
                                                       "{$TREE_ROOT_OUTPUT_DIR}",
                                                       "{$LOCAL_TREE_ROOT_OUTPUT_DIR}",
                                                       "{$OUTPUT_DIR}",
                                                       "{$OUTPUT_FILE}",
                                                       "{$OUTPUT_FILE_NAME}",
                                                       "{$OUTPUT_FILE_EXT}",
                                                       "{$OUTPUT_FILE_EXTS}")

    def __builtin_fsys_vars__dir_dir__main_template_str(self):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="template_path" type="gstr" />
        <var name="index_name" type="gstr" regex="[a-zA-Z0-9_\\.]+" />
    </vars>
    <dir path="{{project_root_dir}}">
        <dir path="stories">
            <dir template="{{template_path}}" />
            <dir path="info">
                <file path="{{index_name}}">
{self.__builtin_fsys_vars__template_vars_list_str()}
                </file>
            </dir>
        </dir>
    </dir>
</template>
        """

    def __builtin_fsys_vars__dir_dir__sub_template_str(self):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="title" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="chapter_name" type="gstr" regex="[a-zA-Z0-9_\\.]+" />
    </vars>
    <dir path="{{title}}">
        <dir path="chapters">
            <file path="{{chapter_name}}">
{self.__builtin_fsys_vars__template_vars_list_str()}
            </file>
        </dir>
    </dir>
</template>
        """

    def test__builtin_fsys_vars__dir_dir__ok(self):
        main_template_filepath = self._make_main_template_filepath()
        main_template_string = self.__builtin_fsys_vars__dir_dir__main_template_str()
        sub_template_filepath = self._make_sub_template_filepath("story_template")
        sub_template_string = self.__builtin_fsys_vars__dir_dir__sub_template_str()
        project_root_dir = "builtin_fsys_vars__dir_dir"
        index_name = "index.draft.txt"
        title = "story_title"
        chapter_name = "new_journey.draft.txt"
        input_parameters = [str(sub_template_filepath), index_name, title, chapter_name]
        self._run__treat_template_xml_file_calling_template__ok(main_template_filepath,
                                                                main_template_string,
                                                                sub_template_filepath,
                                                                sub_template_string,
                                                                project_root_dir,
                                                                input_parameters)
        self.__verify_index_contents(index_name, main_template_filepath, project_root_dir)
        self.__verify_chapter_contents(chapter_name, main_template_filepath, project_root_dir, sub_template_filepath,
                                       title)

    def __verify_index_contents(self, index_name, main_template_filepath, project_root_dir):
        expected_root_output_dirpath = Path(self._output_dirpath)
        expected_tree_root_output_dirpath = expected_root_output_dirpath / project_root_dir
        expected_output_filepath = expected_root_output_dirpath / f"{project_root_dir}/stories/info/{index_name}"
        expected_file_contents = self.__builtin_fsys_vars__vars_list_str(Path.cwd(),
                                                                         main_template_filepath.parent,
                                                                         main_template_filepath.parent,
                                                                         expected_root_output_dirpath,
                                                                         expected_root_output_dirpath,
                                                                         expected_tree_root_output_dirpath,
                                                                         expected_tree_root_output_dirpath,
                                                                         expected_output_filepath.parent,
                                                                         expected_output_filepath,
                                                                         expected_output_filepath.name,
                                                                         expected_output_filepath.suffix,
                                                                         "".join(expected_output_filepath.suffixes))
        self._compare_file_lines_with_expected_lines(expected_output_filepath, expected_file_contents.strip())

    def __verify_chapter_contents(self, chapter_name, main_template_filepath, project_root_dir, sub_template_filepath,
                                  title):
        expected_root_output_dirpath = Path(self._output_dirpath)
        expected_local_root_output_dirpath = expected_root_output_dirpath / f"{project_root_dir}/stories"
        expected_tree_root_output_dirpath = expected_root_output_dirpath / project_root_dir
        expected_local_tree_root_output_dirpath = expected_local_root_output_dirpath / title
        expected_output_filepath = (expected_root_output_dirpath
                                    / f"{project_root_dir}/stories/{title}/chapters/{chapter_name}")
        expected_file_contents = self.__builtin_fsys_vars__vars_list_str(Path.cwd(),
                                                                         main_template_filepath.parent,
                                                                         sub_template_filepath.parent,
                                                                         expected_root_output_dirpath,
                                                                         expected_local_root_output_dirpath,
                                                                         expected_tree_root_output_dirpath,
                                                                         expected_local_tree_root_output_dirpath,
                                                                         expected_output_filepath.parent,
                                                                         expected_output_filepath,
                                                                         expected_output_filepath.name,
                                                                         expected_output_filepath.suffix,
                                                                         "".join(expected_output_filepath.suffixes))
        self._compare_file_lines_with_expected_lines(expected_output_filepath, expected_file_contents.strip())

    def __builtin_fsys_vars__file__template_str(self):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_file" type="gstr" regex="[a-zA-Z0-9_\\.]+" />
    </vars>
    <file path="{{project_file}}">
{self.__builtin_fsys_vars__template_vars_list_str()}
    </file>
</template>
        """

    def test__builtin_fsys_vars__file__ok(self):
        main_template_filepath = self._make_main_template_filepath()
        main_template_string = self.__builtin_fsys_vars__file__template_str()
        project_file = "builtin_fsys_vars__file.txt"
        input_parameters = []
        self._run__treat_template_xml_file__ok(main_template_filepath, main_template_string, project_file,
                                               input_parameters)
        self.__verify_project_file_contents(project_file, main_template_filepath)

    def __verify_project_file_contents(self, file_name, main_template_filepath):
        expected_root_output_dirpath = Path(self._output_dirpath)
        expected_tree_root_output_dirpath = ""
        expected_output_filepath = expected_root_output_dirpath / file_name
        expected_file_contents = self.__builtin_fsys_vars__vars_list_str(Path.cwd(),
                                                                         main_template_filepath.parent,
                                                                         main_template_filepath.parent,
                                                                         expected_root_output_dirpath,
                                                                         expected_root_output_dirpath,
                                                                         expected_tree_root_output_dirpath,
                                                                         expected_tree_root_output_dirpath,
                                                                         expected_output_filepath.parent,
                                                                         expected_output_filepath,
                                                                         expected_output_filepath.name,
                                                                         expected_output_filepath.suffix,
                                                                         "".join(expected_output_filepath.suffixes))
        self._compare_file_lines_with_expected_lines(expected_output_filepath, expected_file_contents.strip())

    @staticmethod
    def __builtin_fsys_vars__dir_file__main_template_str():
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_\\.]+" />
        <var name="template_path" type="gstr" />
    </vars>
    <dir path="{{project_root_dir}}">
        <dir path="docs">
            <file template="{{template_path}}" />
        </dir>
    </dir>
</template>
        """

    def __builtin_fsys_vars__dir_file__sub_template_str(self):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="file_name" type="gstr" regex="[a-zA-Z0-9_\\.]+" />
    </vars>
    <file path="{{file_name}}">
{self.__builtin_fsys_vars__template_vars_list_str()}
    </file>
</template>
        """

    def test__builtin_fsys_vars__dir_file__ok(self):
        main_template_filepath = self._make_main_template_filepath()
        main_template_string = self.__builtin_fsys_vars__dir_file__main_template_str()
        sub_template_filepath = self._make_sub_template_filepath("file_template")
        sub_template_string = self.__builtin_fsys_vars__dir_file__sub_template_str()
        project_root_dir = "builtin_fsys_vars__dir_file"
        file_name = "vars.draft.txt"
        input_parameters = [str(sub_template_filepath), file_name]
        self._run__treat_template_xml_file_calling_template__ok(main_template_filepath,
                                                                main_template_string,
                                                                sub_template_filepath,
                                                                sub_template_string,
                                                                project_root_dir,
                                                                input_parameters)
        self.__verify_vars_file_contents(file_name, main_template_filepath, sub_template_filepath, project_root_dir)

    def __verify_vars_file_contents(self, file_name, main_template_filepath, sub_template_filepath, project_root_dir):
        expected_root_output_dirpath = Path(self._output_dirpath)
        expected_local_root_output_dirpath = expected_root_output_dirpath / project_root_dir / "docs"
        expected_tree_root_output_dirpath = expected_root_output_dirpath / project_root_dir
        expected_local_tree_root_output_dirpath = ""
        expected_output_filepath = expected_root_output_dirpath / project_root_dir / "docs" / file_name
        expected_file_contents = self.__builtin_fsys_vars__vars_list_str(Path.cwd(),
                                                                         main_template_filepath.parent,
                                                                         sub_template_filepath.parent,
                                                                         expected_root_output_dirpath,
                                                                         expected_local_root_output_dirpath,
                                                                         expected_tree_root_output_dirpath,
                                                                         expected_local_tree_root_output_dirpath,
                                                                         expected_output_filepath.parent,
                                                                         expected_output_filepath,
                                                                         expected_output_filepath.name,
                                                                         expected_output_filepath.suffix,
                                                                         "".join(expected_output_filepath.suffixes))
        self._compare_file_lines_with_expected_lines(expected_output_filepath, expected_file_contents.strip())


if __name__ == '__main__':
    unittest.main()
