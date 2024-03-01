import filecmp
import glob
import io
import sys
from pathlib import Path
from unittest import TestCase

from tgen import TemgenProgram


class TestTemgenProgramBase(TestCase):
    __STDIN = sys.stdin
    __TRIVIAL_TEMPLATE_STR = """<?xml version="1.0"?>
<template>
    <vars>
{var_definitions}
    </vars>
    <dir path="{project_root_dir}" {dir_attrs}>
        <file path="data.txt" {file_attrs}>{file_contents}</file>
    </dir>
</template>
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls._output_dirname = "output"
        cls._expected_dirname = "expected"
        cls._generated_input_dirname = "generated_input"
        output_dpath = Path(f"{cls._output_dirname}")
        if output_dpath.exists():
            import shutil
            shutil.rmtree(output_dpath)
        output_dpath.mkdir(parents=True)
        generated_input_dir_path = Path.cwd() / f"{cls._generated_input_dirname}"
        if generated_input_dir_path.exists():
            import shutil
            shutil.rmtree(generated_input_dir_path)
        generated_input_dir_path.mkdir(exist_ok=True)
        cls._ut_context_argv = ['--terminal', '-o', f'{output_dpath}']

    def run(self, result=None):
        assert result is not None
        self.__set_unit_tests_result(result)
        TestCase.run(self, result)  # call superclass run method

    @classmethod
    def __set_unit_tests_result(cls, unit_tests_result):
        cls.__unit_tests_result = unit_tests_result

    @classmethod
    def tearDownClass(cls):
        if len(cls.__unit_tests_result.errors) == 0 and len(cls.__unit_tests_result.failures) == 0:
            import shutil
            output_dpath = Path(f"{cls._output_dirname}")
            shutil.rmtree(output_dpath)
            generated_input_dir_path = Path.cwd() / f"{cls._generated_input_dirname}"
            shutil.rmtree(generated_input_dir_path)

    def _run_generated_trivial_template_file(self, project_root_dir, argv=None, stdin_str=None, **kargs):
        if argv is None:
            argv = []
        generated_template_file_path = self._generate_trivial_template_file(project_root_dir, **kargs)
        temgen = TemgenProgram(self._ut_context_argv + argv + ['--', generated_template_file_path])
        if stdin_str:
            sys.stdin = io.StringIO(stdin_str)
        else:
            sys.stdin = TestTemgenProgramBase.__STDIN
        temgen.run()
        return self._extract_files_contents(project_root_dir)

    def _extract_files_contents(self, project_root_dir):
        root_dir = f"{self._output_dirname}/{project_root_dir}"
        file_list = glob.glob("**/*.txt", root_dir=root_dir, recursive=True)
        file_contents_dict = {}
        for txt_file in file_list:
            with open(f"{root_dir}/{txt_file}") as data_file:
                file_contents_dict[Path(txt_file).as_posix()] = data_file.read()
        return file_contents_dict

    def _test_generated_trivial_template_file(self, project_root_dir, argv=None, stdin_str=None, **kargs):
        if argv is None:
            argv = []
        self._generate_trivial_template_file(project_root_dir, **kargs)
        self._test_generated_template_file(project_root_dir, argv, stdin_str)

    def _test_generated_template_file(self, project_root_dir, argv=None, stdin_str=None):
        if argv is None:
            argv = []
        generated_input_dir_path = Path(f"{self._generated_input_dirname}")
        generated_template_file_path = f'{generated_input_dir_path}/{project_root_dir}.xml'
        temgen = TemgenProgram(self._ut_context_argv + argv + ['--', generated_template_file_path])
        if stdin_str:
            sys.stdin = io.StringIO(stdin_str)
        else:
            sys.stdin = TestTemgenProgramBase.__STDIN
        temgen.run()
        self._compare_output_and_expected(project_root_dir)

    def _generate_trivial_template_file(self, project_root_dir, **kargs):
        keys = ["var_definitions", "dir_attrs", "file_attrs", "file_contents"]
        for key in keys:
            if key not in kargs:
                kargs[key] = ""
        generated_input_dir_path = Path(f"{self._generated_input_dirname}")
        generated_template_file_path = f'{generated_input_dir_path}/{project_root_dir}.xml'
        with open(generated_template_file_path, 'w') as generated_template_file:
            template_contents = self.__TRIVIAL_TEMPLATE_STR.format(project_root_dir=project_root_dir, **kargs)
            generated_template_file.write(template_contents)
        return generated_template_file_path

    def _run_template_file(self, template_filestem, argv=None, stdin_str=None, context_argv=None):
        if argv is None:
            argv = ['--', f'input/{template_filestem}.xml']
        if context_argv is None:
            context_argv = self._ut_context_argv
        temgen = TemgenProgram(context_argv + argv)
        if stdin_str:
            sys.stdin = io.StringIO(stdin_str)
        else:
            sys.stdin = TestTemgenProgramBase.__STDIN
        temgen.run()

    def _test_template_file(self, template_filestem, project_root_dir=None, argv=None, stdin_str=None,
                            context_argv=None):
        if project_root_dir is None:
            project_root_dir = template_filestem
        self._run_template_file(template_filestem, argv, stdin_str, context_argv)
        self._compare_output_and_expected(project_root_dir)

    def _run_template_path_template_versoin(self, template_path, template_version, argv=None, stdin_str=None,
                                            context_argv=None):
        if argv is None:
            argv = ['--', template_path, template_version]
        if context_argv is None:
            context_argv = self._ut_context_argv
        temgen = TemgenProgram(context_argv + argv)
        if stdin_str:
            sys.stdin = io.StringIO(stdin_str)
        else:
            sys.stdin = TestTemgenProgramBase.__STDIN
        temgen.run()

    def _test_template_path_template_version(self, template_path, template_version, project_root_dir,
                                             argv=None, stdin_str=None, context_argv=None):
        self._run_template_path_template_versoin(template_path, template_version, argv, stdin_str, context_argv)
        self._compare_output_and_expected(project_root_dir)

    def _compare_output_and_expected(self, project_root_dir):
        left_dir = f"{self._output_dirname}/{project_root_dir}"
        right_dir = f"{self._expected_dirname}/{project_root_dir}"
        self._compare_directories(filecmp.dircmp(left_dir, right_dir))

    def _compare_directories(self, dcmp):
        if dcmp.diff_files:
            for diff_file in dcmp.diff_files:
                left_path = f"{dcmp.left}/{diff_file}"
                right_path = f"{dcmp.right}/{diff_file}"
                self._diff_files(left_path, right_path)
        if dcmp.common_funny:
            common_funny = [f"{dcmp.right}/{x}" for x in dcmp.common_funny]
            self.assertListEqual([], common_funny)
        if dcmp.funny_files:
            funny_files = [f"{dcmp.right}/{x}" for x in dcmp.funny_files]
            self.assertListEqual([], funny_files)
        if dcmp.right_only:
            right_only = [f"{dcmp.right}/{x}" for x in dcmp.right_only]
            self.assertListEqual([], right_only)
        if dcmp.left_only:
            left_only = [f"{dcmp.left}/{x}" for x in dcmp.left_only]
            self.assertListEqual([], left_only)
        # recurse:
        for sub_dcmp in dcmp.subdirs.values():
            self._compare_directories(sub_dcmp)

    def _diff_files(self, left_path, right_path):
        print("### start of _diff_files ###")
        import difflib
        with open(left_path) as left_file:
            left_text = left_file.readlines()
        with open(right_path) as right_file:
            right_text = right_file.readlines()
        # Find and print the diff:
        for line in difflib.unified_diff(left_text, right_text,
                                         fromfile=left_path, tofile=right_path):
            print(line.rstrip())
            if line.startswith('---') or line.startswith('+++') or line.startswith(' '):
                continue
            assert len(line) > 0
            if line[0] == '+':
                self.fail(f"Difference met while comparing:\n  '{left_path}' and\n  '{right_path}'.")
        self.fail(f"Difference met while comparing:\n  '{left_path}' and\n  '{right_path}'.")
