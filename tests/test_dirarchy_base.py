import filecmp
import io
import sys
from pathlib import Path
from unittest import TestCase

from main import Dirarchy


class TestDirarchyBase(TestCase):
    __STDIN = sys.stdin
    __TRIVIAL_DIRARCHY_STR = """<?xml version="1.0"?>
<dirarchy>
    <vars>
{vars_definitions}
    </vars>
    <dir path="{project_root_dir}" {dir_attrs}>
        <file path="data.txt" {file_attrs}>{file_contents}</file>
    </dir>
</dirarchy>
    """

    def setUp(self):
        self._output_dirname = "output"
        self._expected_dirname = "expected"
        self._generated_input_dirname = "generated_input"
        output_dpath = Path(f"{self._output_dirname}")
        if output_dpath.exists():
            import shutil
            shutil.rmtree(output_dpath)
        output_dpath.mkdir(parents=True)
        generated_input_dir_path = Path.cwd() / f"{self._generated_input_dirname}"
        if generated_input_dir_path.exists():
            import shutil
            shutil.rmtree(generated_input_dir_path)
        generated_input_dir_path.mkdir(exist_ok=True)
        self._ut_context_argv = ['--terminal', '-d', f'{output_dpath}']

    def _run_generated_trivial_dirarchy_file(self, project_root_dir, argv=None, stdin_str=None, **kargs):
        if argv is None:
            argv = []
        generated_dirarchy_file_path = self._generate_trivial_dirarchy_file(project_root_dir, **kargs)
        dirarchy = Dirarchy(self._ut_context_argv + argv + ['--', generated_dirarchy_file_path])
        if stdin_str:
            sys.stdin = io.StringIO(stdin_str)
        else:
            sys.stdin = TestDirarchyBase.__STDIN
        dirarchy.run()
        with open(f"{self._output_dirname}/{project_root_dir}/data.txt") as data_file:
            return data_file.read()

    def _test_generated_trivial_dirarchy_file(self, project_root_dir, argv=None, stdin_str=None, **kargs):
        if argv is None:
            argv = []
        self._generate_trivial_dirarchy_file(project_root_dir, **kargs)
        self._test_generated_dirarchy_file(project_root_dir, argv, stdin_str)

    def _test_generated_dirarchy_file(self, project_root_dir, argv=None, stdin_str=None):
        if argv is None:
            argv = []
        generated_input_dir_path = Path(f"{self._generated_input_dirname}")
        generated_dirarchy_file_path = f'{generated_input_dir_path}/{project_root_dir}.xml'
        dirarchy = Dirarchy(self._ut_context_argv + argv + ['--', generated_dirarchy_file_path])
        self.__run_dirarchy_and_check_output(dirarchy, project_root_dir, stdin_str)

    def _generate_trivial_dirarchy_file(self, project_root_dir, **kargs):
        keys = ["vars_definitions", "dir_attrs", "file_attrs", "file_contents"]
        for key in keys:
            if key not in kargs:
                kargs[key] = ""
        generated_input_dir_path = Path(f"{self._generated_input_dirname}")
        generated_dirarchy_file_path = f'{generated_input_dir_path}/{project_root_dir}.xml'
        with open(generated_dirarchy_file_path, 'w') as generated_dirarchy_file:
            dirarchy_contents = self.__TRIVIAL_DIRARCHY_STR.format(project_root_dir=project_root_dir, **kargs)
            generated_dirarchy_file.write(dirarchy_contents)
        return generated_dirarchy_file_path

    def __run_dirarchy_and_check_output(self, dirarchy: Dirarchy, project_root_dir, stdin_str):
        if stdin_str:
            sys.stdin = io.StringIO(stdin_str)
        else:
            sys.stdin = TestDirarchyBase.__STDIN
        dirarchy.run()
        self._compare_output_and_expected(project_root_dir)

    def _test_dirarchy_file(self, project_root_dir, argv=None, stdin_str=None):
        if argv is None:
            argv = ['--', f'input/{project_root_dir}.xml']
        dirarchy = Dirarchy(self._ut_context_argv + argv)
        self.__run_dirarchy_and_check_output(dirarchy, project_root_dir, stdin_str)

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
