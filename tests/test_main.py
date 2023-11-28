import datetime
from pathlib import Path

from tests.test_dirarchy_base import TestDirarchyBase


class TestDirarchy(TestDirarchyBase):
    def test_simple_dirtree(self):
        self._test_dirarchy_file("simple_dirtree")

    def test_simple_fdirtree(self):
        self._test_dirarchy_file("simple_fdirtree", stdin_str='arba\ncore')

    def test_trivial_fdirtree__bad_format_str__exception(self):
        try:
            self._run_generated_trivial_dirarchy_file("bad_format_str", file_contents="{whut")
            self.fail()
        except ValueError as err:
            self.assertEqual(str(err), "expected '}' before end of string")

    def test_trivial_fdirtree__unknown_var__exception(self):
        try:
            self._run_generated_trivial_dirarchy_file("unknown_var", file_contents="{unknown_var}")
            self.fail()
        except KeyError:
            pass

    def test_trivial_fdirtree__builtin_CURRENT_SOURCE_DIR__exception(self):
        project_root_dir = "builtin_CURRENT_SOURCE_DIR"
        f_contents = "{$CURRENT_SOURCE_DIR}"
        extracted_value = self._run_generated_trivial_dirarchy_file(project_root_dir, file_contents=f_contents)
        extracted_value = Path(extracted_value).resolve()
        expected_value = (Path.cwd() / self._generated_input_dirname).resolve()
        self.assertEqual(extracted_value, expected_value)

    def test_trivial_fdirtree__builtin_date_vars__exception(self):
        project_root_dir = "builtin_date_vars"
        f_contents = "{$YEAR},{$MONTH},{$DAY},{$DATE_YMD},{$DATE_Y_M_D}"
        extracted_value = self._run_generated_trivial_dirarchy_file(project_root_dir, file_contents=f_contents)
        expected_value = datetime.date.today().strftime("%Y,%m,%d,%Y%m%d,%Y-%m-%d")
        self.assertEqual(extracted_value, expected_value)
