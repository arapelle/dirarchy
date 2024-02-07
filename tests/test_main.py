import datetime
import shutil
import sys
import unittest
from json import JSONDecodeError
from pathlib import Path

from tests.test_dirarchy_base import TestDirarchyBase
from main import Dirarchy


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

    def test__if_fdirtree__invalid_missing_then__exception(self):
        try:
            output_root_dir = "if_fdirtree__invalid_missing_then"
            in_str = f'{output_root_dir}\nyes'
            self._test_dirarchy_file(output_root_dir, stdin_str=in_str)
            self.fail()
        except Exception as ex:
            self.assertEqual(str(ex), "A 'else' node is provided for a 'if' node but a 'then' node is missing.")

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
            context_argv = ['--terminal', '-o', f'__not_found__']
            output_root_dir = "cli_args__invalid_output_dir"
            in_str = f'{output_root_dir}\nok\nok'
            self._test_dirarchy_file("simple_fdirtree", project_root_dir=output_root_dir, stdin_str=in_str,
                                     context_argv=context_argv)
            self.fail()
        except Exception as ex:
            self.assertEqual(str(ex), "The provided output directory does not exist: '__not_found__'.")

    def test__cli_args__valid_v__ok(self):
        output_root_dir = "cli_args__valid_v"
        args = ['--var', 'text=coucou', 'other_text=']
        var_defs = '<var name="text" />\n<var name="other_text" />'
        self._test_generated_trivial_dirarchy_file(output_root_dir, argv=args,
                                                   var_definitions=var_defs, file_contents=":{text}:{other_text}:")

    def test__cli_args__valid_var__ok(self):
        output_root_dir = "cli_args__valid_var"
        args = ['--var', 'text=coucou', 'other_text=']
        var_defs = '<var name="text" />\n<var name="other_text" />'
        self._test_generated_trivial_dirarchy_file(output_root_dir, argv=args,
                                                   var_definitions=var_defs, file_contents=":{text}:{other_text}:")

    def test__cli_args__valid_var_override__ok(self):
        output_root_dir = "cli_args__valid_var_override"
        args = ['--var', 'text=good_value', 'other_text=']
        var_defs = '<var name="text" value="bad_value" />\n<var name="other_text" />'
        self._test_generated_trivial_dirarchy_file(output_root_dir, argv=args,
                                                   var_definitions=var_defs, file_contents=":{text}:{other_text}:")

    def test__cli_args__invalid_v__exception(self):
        bad_var = 'bad-var=coucou'
        try:
            output_root_dir = "cli_args__invalid_v"
            args = ['-v', 'text=coucou', bad_var]
            var_defs = '<var name="text" value="{text}" />'
            self._run_generated_trivial_dirarchy_file(output_root_dir, argv=args,
                                                      var_definitions=var_defs, file_contents="{text}")
            self.fail()
        except RuntimeError as err:
            self.assertEqual(str(err), bad_var)

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

    def test__var_file__valid_var_file__ok(self):
        output_root_dir = "var_file__valid_var_file"
        args = ['--var-file', 'input/var_files/texts.json']
        var_defs = '<var name="text" />\n<var name="other_text" />'
        self._test_generated_trivial_dirarchy_file(output_root_dir, argv=args,
                                                   var_definitions=var_defs, file_contents=":{text}:{other_text}:")

    def test__var_file__unknown_var_file__exception(self):
        json_fpath = 'input/var_files/not_found.json'
        try:
            output_root_dir = "var_file__unknown_var_file"
            args = ['--var-file', json_fpath]
            self._run_generated_trivial_dirarchy_file(output_root_dir, argv=args)
            self.fail()
        except FileNotFoundError as err:
            self.assertTrue(str(err).find(f"No such file or directory: '{json_fpath}'") != -1)

    def test__var_file__bad_var_file__exception(self):
        json_fpath = 'input/var_files/bad.json'
        try:
            output_root_dir = "var_file__bad_var_file"
            args = ['--var-file', json_fpath]
            var_defs = '<var name="text" />\n<var name="other_text" />'
            self._run_generated_trivial_dirarchy_file(output_root_dir, argv=args,
                                                      var_definitions=var_defs, file_contents=":{text}:{other_text}:")
            self.fail()
        except JSONDecodeError:
            pass

    def test__custom_ui__valid_cmd__ok(self):
        output_root_dir = "custom_ui__valid_cmd"
        args = ['-C', f'{sys.executable} input/custom_ui/myui.py']
        var_defs = '<var name="text" value="good_value" />\n<var name="other_text" value="" />'
        self._test_generated_trivial_dirarchy_file(output_root_dir, argv=args,
                                                   var_definitions=var_defs, file_contents=":{text}:{other_text}:")

    def test__custom_ui__invalid_cmd__exception(self):
        try:
            output_root_dir = "custom_ui__invalid_cmd"
            args = ['-C', f'{sys.executable} input/custom_ui/not_found.py']
            var_defs = '<var name="text" value="good_value" />\n<var name="other_text" value="" />'
            self._run_generated_trivial_dirarchy_file(output_root_dir, argv=args,
                                                      var_definitions=var_defs, file_contents=":{text}:{other_text}:")
        except RuntimeError as err:
            self.assertTrue(str(err).find("Execution of custom ui did not work well") != -1)

    def test__file_fdirtree__format_raw__ok(self):
        output_root_dir = "file_fdirtree__format_raw"
        in_str = f'{output_root_dir}\nraw\nunused_message'
        self._test_dirarchy_file("file_fdirtree__valid_format", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_fdirtree__copy_raw__ok(self):
        output_root_dir = "file_fdirtree__copy_raw"
        in_str = f'{output_root_dir}\nfruits.txt\nraw\nPeer'
        self._test_dirarchy_file("file_fdirtree__copy", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_fdirtree__copy_format__ok(self):
        output_root_dir = "file_fdirtree__copy_format"
        in_str = f'{output_root_dir}\nfruits.txt\nformat\nPear'
        self._test_dirarchy_file("file_fdirtree__copy", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_fdirtree__copy_bad_file__exception(self):
        filename = "unknown.txt"
        try:
            output_root_dir = "file_fdirtree__copy_bad_file"
            in_str = f'{output_root_dir}\n{filename}\nformat\nPear'
            self._test_dirarchy_file("file_fdirtree__copy", project_root_dir=output_root_dir, stdin_str=in_str)
            self.fail()
        except FileNotFoundError as err:
            self.assertTrue(str(err).find(f"{filename}") != -1)

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

    @classmethod
    def setUpClass(cls) -> None:
        TestDirarchyBase.setUpClass()
        template_local_root = "temfile"
        template_root = Path(f"{Dirarchy.system_template_roots()[-1]}/{template_local_root}")
        template_root.mkdir(parents=True, exist_ok=True)
        shutil.copyfile("input/templates/temfile-1.0.0.xml", f"{template_root}/temfile-1.0.0.xml")
        shutil.copyfile("input/templates/temfile-1.1.0.xml", f"{template_root}/temfile-1.1.0.xml")
        shutil.copyfile("input/templates/temfile-1.1.1.xml", f"{template_root}/temfile-1.1.1.xml")
        shutil.copyfile("input/templates/temfile-1.2.0.xml", f"{template_root}/temfile-1.2.0.xml")
        shutil.copyfile("input/templates/temfile-2.0.0.xml", f"{template_root}/temfile-2.0.0.xml")
        template_local_root = "temdir"
        template_root = Path(f"{Dirarchy.system_template_roots()[-1]}/{template_local_root}")
        template_root.mkdir(parents=True, exist_ok=True)
        shutil.copyfile("input/templates/temdir-1.0.0.xml", f"{template_root}/temdir-1.0.0.xml")
        shutil.copyfile("input/templates/temdir.xml", f"{template_root}/temdir.xml")

    def test__dir_template__local_xml__ok(self):
        output_root_dir = "dir_template__valid_local_xml"
        in_str = f'{output_root_dir}\ninput/templates\ntemdir-1.0.0.xml\nmy_equipment'
        self._test_dirarchy_file("dir_template__valid", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__dir_template__global_xml__ok(self):
        output_root_dir = "dir_template__valid_global_xml"
        in_str = f'{output_root_dir}\ntemdir\ntemdir-1.0.0.xml\nmy_equipment'
        self._test_dirarchy_file("dir_template__valid", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_template__local_xml__ok(self):
        output_root_dir = "file_template__valid_local_xml"
        in_str = f'{output_root_dir}\ninput/templates\ntemfile-1.0.0.xml\nobject.txt\nsword'
        self._test_dirarchy_file("file_template__valid", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_template__local_xml_ver__warning(self):
        output_root_dir = "file_template__valid_local_xml_ver"
        in_str = f'{output_root_dir}\ninput/templates\ntemfile-1.0.0.xml\n1.0.0\nobject.txt\nsword'
        self._test_dirarchy_file("file_template__valid_ver", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_template__global_xml__ok(self):
        output_root_dir = "file_template__valid_global_xml"
        in_str = f'{output_root_dir}\ntemfile\ntemfile-1.0.0.xml\nobject.txt\nsword'
        self._test_dirarchy_file("file_template__valid", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_template__local_path_1_1_0__ok(self):
        output_root_dir = "file_template__valid_local_path_1_1_0"
        in_str = f'{output_root_dir}\ninput/templates\ntemfile\n1.1.0\nobject.txt\nsword'
        self._test_dirarchy_file("file_template__valid_ver", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_template__local_path_1_1__ok(self):
        output_root_dir = "file_template__valid_local_path_1_1"
        in_str = f'{output_root_dir}\ninput/templates\ntemfile\n1.1\nobject.txt\nsword'
        self._test_dirarchy_file("file_template__valid_ver", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_template__local_path_1__ok(self):
        output_root_dir = "file_template__valid_local_path_1"
        in_str = f'{output_root_dir}\ninput/templates\ntemfile\n1\nobject.txt\nsword'
        self._test_dirarchy_file("file_template__valid_ver", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_template__global_path_1_1_0__ok(self):
        output_root_dir = "file_template__valid_global_path_1_1_0"
        in_str = f'{output_root_dir}\ntemfile\ntemfile\n1.1.0\nobject.txt\nsword'
        self._test_dirarchy_file("file_template__valid_ver", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_template__global_path_1_1__ok(self):
        output_root_dir = "file_template__valid_global_path_1_1"
        in_str = f'{output_root_dir}\ntemfile\ntemfile\n1.1\nobject.txt\nsword'
        self._test_dirarchy_file("file_template__valid_ver", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_template__global_path_1__ok(self):
        output_root_dir = "file_template__valid_global_path_1"
        in_str = f'{output_root_dir}\ntemfile\ntemfile\n1\nobject.txt\nsword'
        self._test_dirarchy_file("file_template__valid_ver", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_template__local_path_4_0_4__err(self):
        filename = "temfile"
        try:
            output_root_dir = "file_template__invalid_local_path_4_0_4"
            in_str = f'{output_root_dir}\ninput/templates\n{filename}\n4.0.4\nobject.txt\nsword'
            self._test_dirarchy_file("file_template__valid_ver", project_root_dir=output_root_dir, stdin_str=in_str)
        except RuntimeError as err:
            self.assertTrue(str(err).startswith("No template "))
            self.assertTrue(str(err).find(f"compatible with version ") != -1)
            self.assertTrue(str(err).find(f"{filename}") != -1)

    def test__file_template__local_path_last__ok(self):
        output_root_dir = "file_template__valid_local_path_last"
        in_str = f'{output_root_dir}\ninput/templates\ntemfile\nobject.txt\nsword\nshield'
        self._test_dirarchy_file("file_template__valid", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__file_template__global_path_last__ok(self):
        output_root_dir = "file_template__valid_global_path_last"
        in_str = f'{output_root_dir}\ntemfile\ntemfile\nobject.txt\nsword\nshield'
        self._test_dirarchy_file("file_template__valid", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__dir_template__local_path_xml__ok(self):
        output_root_dir = "dir_template__valid_local_path_xml"
        in_str = f'{output_root_dir}\ninput/templates\ntemdir\nmy_equipment'
        self._test_dirarchy_file("dir_template__valid", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__dir_template__global_path_xml__ok(self):
        output_root_dir = "dir_template__valid_global_path_xml"
        in_str = f'{output_root_dir}\ntemdir\ntemdir\nmy_equipment'
        self._test_dirarchy_file("dir_template__valid", project_root_dir=output_root_dir, stdin_str=in_str)

    def test__dir_template__invalid_path_ver_wo_ext__err(self):
        filename = "temdir-1.0.0"
        try:
            output_root_dir = "dir_template__invalid_local_path_xml"
            in_str = f'{output_root_dir}\ninput/templates\n{filename}\nmy_equipment'
            self._test_dirarchy_file("dir_template__valid", project_root_dir=output_root_dir, stdin_str=in_str)
            self.fail()
        except RuntimeError as err:
            self.assertTrue(str(err).startswith("The extension '.xml' is missing at the end of the template path: "))
            self.assertTrue(str(err).find(f"{filename}") != -1)

    def test__dir_template__invalid_xml__err(self):
        filename = "notfound.xml"
        try:
            output_root_dir = "dir_template__invalid_xml"
            in_str = f'{output_root_dir}\ninput/templates\n{filename}\nmy_equipment'
            self._test_dirarchy_file("dir_template__valid", project_root_dir=output_root_dir, stdin_str=in_str)
            self.fail()
        except RuntimeError as err:
            self.assertTrue(str(err).startswith("Template not found: "))
            self.assertTrue(str(err).find(f"{filename}") != -1)

    def test__vars_bool__y_Y_True__ok(self):
        output_root_dir = "vars_bool__y_Y_True"
        var_defs = '<var name="first" type="bool" />'
        var_defs += '<var name="second" type="bool" />'
        var_defs += '<var name="third" type="bool" />'
        in_str = "f\nfalse\nno\ny\nY\nTrue"
        self._test_generated_trivial_dirarchy_file(output_root_dir, stdin_str=in_str, var_definitions=var_defs,
                                                   file_contents="{first}\n{second}\n{third}\n")

    def test__vars_bool__n_N_False__ok(self):
        output_root_dir = "vars_bool__n_N_False"
        var_defs = '<var name="first" type="bool" />'
        var_defs += '<var name="second" type="bool" />'
        var_defs += '<var name="third" type="bool" />'
        in_str = "t\ntrue\nyes\nn\nN\nFalse"
        self._test_generated_trivial_dirarchy_file(output_root_dir, stdin_str=in_str, var_definitions=var_defs,
                                                   file_contents="{first}\n{second}\n{third}\n")

    def test__vars_int__ints__ok(self):
        output_root_dir = "vars_int__ints"
        var_defs = '<var name="first" type="int" />'
        var_defs += '<var name="second" type="int" />'
        in_str = "7t\n42.5\n36\n-42.5\n-37"
        self._test_generated_trivial_dirarchy_file(output_root_dir, stdin_str=in_str, var_definitions=var_defs,
                                                   file_contents="{first}\n{second}\n")


if __name__ == '__main__':
    unittest.main()
