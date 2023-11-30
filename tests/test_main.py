import datetime
import unittest
from pathlib import Path

from tests.test_dirarchy_base import TestDirarchyBase


class TestDirarchy(TestDirarchyBase):
    def test__simple_dirtree__valid__ok(self):
        self._test_dirarchy_file("simple_dirtree")

    def test__simple_fdirtree__valid__ok(self):
        self._test_dirarchy_file("simple_fdirtree", stdin_str='arba\ncore')

    def test__if_fdirtree__valid_yes_yes__ok(self):
        output_root_dir = "if_valid_yes_yes"
        in_str = f'{output_root_dir}\nyes\nyes'
        self._test_dirarchy_file("if_fdirtree__valid", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__if_fdirtree__valid_yes_no__ok(self):
        output_root_dir = "if_valid_yes_no"
        in_str = f'{output_root_dir}\nyes\nno'
        self._test_dirarchy_file("if_fdirtree__valid", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__if_fdirtree__valid_no_no__ok(self):
        output_root_dir = "if_valid_no_no"
        in_str = f'{output_root_dir}\nno\nno'
        self._test_dirarchy_file("if_fdirtree__valid", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__if_fdirtree__invalid_two_then__exception(self):
        try:
            output_root_dir = "if_fdirtree__invalid_two_then"
            in_str = f'{output_root_dir}\nyes'
            self._test_dirarchy_file(output_root_dir, stdin_str=in_str)
            self.fail()
        except Exception as ex:
            self.assertEqual(str(ex), "Too many 'then' nodes for a 'if' node.")

    def test__if_fdirtree__invalid_two_else__exception(self):
        try:
            output_root_dir = "if_fdirtree__invalid_two_else"
            in_str = f'{output_root_dir}\nyes'
            self._test_dirarchy_file(output_root_dir, stdin_str=in_str)
            self.fail()
        except Exception as ex:
            self.assertEqual(str(ex), "Too many 'else' nodes for a 'if' node.")

    def test__match_fdirtree__valid_value__ok(self):
        output_root_dir = "match_valid_value"
        in_str = f'{output_root_dir}\nvalue'
        self._test_dirarchy_file("match_fdirtree__valid_with_default",
                                 project_root_dir=output_root_dir, stdin_str=in_str)

    def test__match_fdirtree__valid_expr_09__ok(self):
        output_root_dir = "match_valid_expr_09"
        in_str = f'{output_root_dir}\n1235'
        self._test_dirarchy_file("match_fdirtree__valid_with_default",
                                 project_root_dir=output_root_dir, stdin_str=in_str)

    def test__match_fdirtree__valid_default__ok(self):
        output_root_dir = "match_valid_default"
        in_str = f'{output_root_dir}\ndefault_case'
        self._test_dirarchy_file("match_fdirtree__valid_with_default",
                                 project_root_dir=output_root_dir, stdin_str=in_str)

    def test__match_fdirtree__valid_no_match__ok(self):
        output_root_dir = "match_valid_no_match"
        in_str = f'{output_root_dir}\nno_match'
        self._test_dirarchy_file("match_fdirtree__valid_without_default",
                                 project_root_dir=output_root_dir, stdin_str=in_str)

    def test__match_fdirtree__invalid_two_default__exception(self):
        try:
            output_root_dir = "match_fdirtree__invalid_two_default"
            in_str = f'{output_root_dir}\nno_match'
            self._test_dirarchy_file(output_root_dir, stdin_str=in_str)
            self.fail()
        except Exception as ex:
            self.assertEqual(str(ex), "A match node cannot have two default case nodes.")

    def test__match_fdirtree__invalid_missing_case__exception(self):
        try:
            output_root_dir = "match_fdirtree__invalid_missing_case"
            in_str = f'{output_root_dir}\nno_match'
            self._test_dirarchy_file(output_root_dir, stdin_str=in_str)
            self.fail()
        except Exception as ex:
            self.assertEqual(str(ex), "case nodes are missing in match node.")

    def test__cli_args__invalid_output_dir__exception(self):
        try:
            context_argv = ['--terminal', '-d', f'__not_found__']
            output_root_dir = "cli_args__invalid_output_dir"
            in_str = f'{output_root_dir}\nok\nok'
            self._test_dirarchy_file("simple_fdirtree", project_root_dir=output_root_dir, stdin_str=in_str,
                                     context_argv=context_argv)
            self.fail()
        except Exception as ex:
            self.assertEqual(str(ex), "The provided output directory does not exist: '__not_found__'.")

    def test__trivial_dirarchy__bad_format_str__exception(self):
        try:
            self._run_generated_trivial_dirarchy_file("bad_format_str", file_contents="{whut")
            self.fail()
        except ValueError as err:
            self.assertEqual(str(err), "expected '}' before end of string")

    def test__trivial_dirarchy__unknown_var__exception(self):
        try:
            self._run_generated_trivial_dirarchy_file("unknown_var", file_contents="{unknown_var}")
            self.fail()
        except KeyError:
            pass

    def test__trivial_fdirtree__builtin_CURRENT_SOURCE_DIR__exception(self):
        project_root_dir = "builtin_CURRENT_SOURCE_DIR"
        f_contents = "{$CURRENT_SOURCE_DIR}"
        extracted_value = self._run_generated_trivial_dirarchy_file(project_root_dir, file_contents=f_contents)
        extracted_value = Path(extracted_value).resolve()
        expected_value = (Path.cwd() / self._generated_input_dirname).resolve()
        self.assertEqual(extracted_value, expected_value)

    def test__trivial_fdirtree__builtin_date_vars__exception(self):
        project_root_dir = "builtin_date_vars"
        f_contents = "{$YEAR},{$MONTH},{$DAY},{$DATE_YMD},{$DATE_Y_M_D}"
        extracted_value = self._run_generated_trivial_dirarchy_file(project_root_dir, file_contents=f_contents)
        expected_value = datetime.date.today().strftime("%Y,%m,%d,%Y%m%d,%Y-%m-%d")
        self.assertEqual(extracted_value, expected_value)


if __name__ == '__main__':
    unittest.main()
