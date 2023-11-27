import filecmp
import io
import sys
from pathlib import Path
from unittest import TestCase

from main import Dirarchy


class TestDirarchyBase(TestCase):
    __STDIN = sys.stdin

    def setUp(self):
        self._output_dirname = "output"
        self._expected_dirname = "expected"
        output_dpath = Path.cwd() / f"{self._output_dirname}"
        if output_dpath.exists():
            import shutil
            shutil.rmtree(output_dpath)
        self._ut_context_argv = ['--terminal', '-d', f'{output_dpath}']

    def _test_dirarchy_expect_success(self, project_root_dir, argv=None, stdin_str=None):
        if argv is None:
            argv = ['--', f'input/{project_root_dir}.xml']
        dirarchy = Dirarchy(self._ut_context_argv + argv)
        if stdin_str:
            sys.stdin = io.StringIO(stdin_str)
        else:
            sys.stdin = TestDirarchyBase.__STDIN
        dirarchy.run()
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
