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
