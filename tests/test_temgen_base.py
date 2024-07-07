import io
import sys
from pathlib import Path

from cli_temgen import CliTemgen
from util import random_string
from ui.basic.terminal_basic_ui import TerminalBasicUi
from temgen import Temgen
from tests.dircmp_test_case import DirCmpTestCase


class TestTemgenBase(DirCmpTestCase):
    TMP_DIR_PATH = Path.cwd() / "tmp"
    MAIN_TEMPLATE_DIR_PATH = TMP_DIR_PATH / "input/templates/main"
    SUB_TEMPLATE_DIR_PATH = MAIN_TEMPLATE_DIR_PATH / "sub"

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.removeDirIfSuccess(cls.TMP_DIR_PATH)

    def _make_main_template_filepath(self):
        main_template_dirpath = self.MAIN_TEMPLATE_DIR_PATH
        main_template_filepath = main_template_dirpath / f"template_{random_string.random_lower_sisy_string(8)}.xml"
        return main_template_filepath

    def _make_sub_template_filepath(self, sub_template_name: str):
        sub_template_dirpath = self.SUB_TEMPLATE_DIR_PATH
        sub_template_filepath = sub_template_dirpath / f"{sub_template_name}.xml"
        return sub_template_filepath

    @staticmethod
    def _make_template_file(template_filepath: Path, template_string: str):
        template_filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(template_filepath, "w") as template_file:
            template_file.write(template_string)

    @staticmethod
    def _read_output_file_contents(output_filepath: Path):
        with open(output_filepath) as result_file:
            return result_file.read().strip()

    def _test__treat_template_xml_string__ok(self,
                                             template_string: str,
                                             project_root_dir: str,
                                             input_parameters: list,
                                             ui: str | None = None,
                                             **kargs):
        input_parameters_str = "\n".join(input_parameters)
        sys.stdin = io.StringIO(f"{project_root_dir}\n{input_parameters_str}")
        template_generator = Temgen(TerminalBasicUi(), **kargs)
        template_generator.treat_template_xml_string(template_string, output_dir=Path(self._output_dirpath), ui=ui)
        self._compare_output_and_expected(project_root_dir)

    def _test__treat_template_xml_string__exception(self,
                                                    template_string: str,
                                                    project_root_dir: str,
                                                    input_parameters: list,
                                                    **kargs):
        input_parameters_str = "\n".join(input_parameters)
        sys.stdin = io.StringIO(f"{project_root_dir}\n{input_parameters_str}")
        template_generator = Temgen(TerminalBasicUi(), **kargs)
        template_generator.treat_template_xml_string(template_string, output_dir=Path(self._output_dirpath))
        self.fail()

    def _test__treat_template_xml_string_calling_template__ok(self,
                                                              main_template_string: str,
                                                              sub_template_filepath: Path,
                                                              sub_template_string: str,
                                                              project_root_dir: str,
                                                              input_parameters: list,
                                                              **kargs):
        try:
            self._make_template_file(sub_template_filepath, sub_template_string)
            self._test__treat_template_xml_string__ok(main_template_string, project_root_dir, input_parameters, **kargs)
        finally:
            sub_template_filepath.unlink(missing_ok=True)

    def _test__treat_template_xml_string_calling_template__exception(self,
                                                                     main_template_string: str,
                                                                     sub_template_filepath: Path,
                                                                     sub_template_string: str,
                                                                     project_root_dir: str,
                                                                     input_parameters: list,
                                                                     **kargs):
        try:
            self._make_template_file(sub_template_filepath, sub_template_string)
            self._test__treat_template_xml_string__exception(main_template_string, project_root_dir, input_parameters,
                                                             **kargs)
        finally:
            sub_template_filepath.unlink(missing_ok=True)

    def _run__treat_template_xml_string__file_contents__ok(self,
                                                           file_contents: str,
                                                           project_root_dir: str,
                                                           input_parameters: list,
                                                           **kargs):
        template_string = f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt">
{file_contents}
        </file>
    </dir>
</template>
        """
        input_parameters_str = "\n".join(input_parameters)
        sys.stdin = io.StringIO(f"{project_root_dir}\n{input_parameters_str}")
        template_generator = Temgen(TerminalBasicUi(), **kargs)
        template_generator.treat_template_xml_string(template_string, output_dir=Path(self._output_dirpath))
        with open(f"{self._output_dirpath}/{project_root_dir}/data.txt") as output_file:
            return output_file.read().strip()

    def _run__treat_template_xml_file__ok(self,
                                          template_filepath: Path,
                                          template_string: str,
                                          project_root_dir: str,
                                          input_parameters: list,
                                          **kargs):
        try:
            self._make_template_file(template_filepath, template_string)
            input_parameters_str = "\n".join(input_parameters)
            sys.stdin = io.StringIO(f"{project_root_dir}\n{input_parameters_str}")
            template_generator = Temgen(TerminalBasicUi(), **kargs)
            template_generator.treat_template_file(template_filepath, output_dir=Path(self._output_dirpath))
        finally:
            template_filepath.unlink(missing_ok=True)

    def _run__treat_template_xml_file_calling_template__ok(self,
                                                           main_template_filepath: Path,
                                                           main_template_string: str,
                                                           sub_template_filepath: Path,
                                                           sub_template_string: str,
                                                           project_root_dir: str,
                                                           input_parameters: list,
                                                           **kargs):
        try:
            self._make_template_file(main_template_filepath, main_template_string)
            self._make_template_file(sub_template_filepath, sub_template_string)
            input_parameters_str = "\n".join(input_parameters)
            sys.stdin = io.StringIO(f"{project_root_dir}\n{input_parameters_str}")
            template_generator = Temgen(TerminalBasicUi(), **kargs)
            template_generator.treat_template_file(main_template_filepath, output_dir=Path(self._output_dirpath))
        finally:
            main_template_filepath.unlink(missing_ok=True)
            sub_template_filepath.unlink(missing_ok=True)

    def _test__treat_template_xml_file__ok(self,
                                           template_filepath: Path,
                                           template_string: str,
                                           project_root_dir: str,
                                           input_parameters: list,
                                           **kargs):
        self._run__treat_template_xml_file__ok(template_filepath, template_string, project_root_dir,
                                               input_parameters, **kargs)
        self._compare_output_and_expected(project_root_dir)

    def _test__treat_template_xml_file__exception(self,
                                                  template_filepath: Path,
                                                  template_string: str,
                                                  project_root_dir: str,
                                                  input_parameters: list,
                                                  **kargs):
        self._run__treat_template_xml_file__ok(template_filepath, template_string, project_root_dir,
                                               input_parameters, **kargs)
        self.fail()

    def _test__treat_template_xml_file_calling_template__ok(self,
                                                            main_template_filepath: Path,
                                                            main_template_string: str,
                                                            sub_template_filepath: Path,
                                                            sub_template_string: str,
                                                            project_root_dir: str,
                                                            input_parameters: list,
                                                            **kargs):
        self._run__treat_template_xml_file_calling_template__ok(main_template_filepath,
                                                                main_template_string,
                                                                sub_template_filepath,
                                                                sub_template_string,
                                                                project_root_dir,
                                                                input_parameters,
                                                                **kargs)
        self._compare_output_and_expected(project_root_dir)

    def _test__treat_template_xml_file_calling_template__exception(self,
                                                                   main_template_filepath: Path,
                                                                   main_template_string: str,
                                                                   sub_template_filepath: Path,
                                                                   sub_template_string: str,
                                                                   project_root_dir: str,
                                                                   input_parameters: list,
                                                                   **kargs):
        self._run__treat_template_xml_file_calling_template__ok(main_template_filepath,
                                                                main_template_string,
                                                                sub_template_filepath,
                                                                sub_template_string,
                                                                project_root_dir,
                                                                input_parameters,
                                                                **kargs)
        self.fail()

    def _run__cli_temgen__treat_template_file__ok(self,
                                                  template_filepath: Path,
                                                  argv: list[str],
                                                  project_root_dir: str,
                                                  input_parameters: list):
        argv.extend(["--", template_filepath])
        cli_temgen = CliTemgen(argv)
        input_parameters_str = "\n".join(input_parameters)
        sys.stdin = io.StringIO(f"{project_root_dir}\n{input_parameters_str}")
        cli_temgen.run()

    def _run__cli_temgen__treat_template_string__ok(self,
                                                    template_string: str,
                                                    argv: list[str],
                                                    project_root_dir: str,
                                                    input_parameters: list):
        template_filepath = self._make_main_template_filepath()
        self._make_template_file(template_filepath, template_string)
        self._run__cli_temgen__treat_template_file__ok(template_filepath, argv, project_root_dir, input_parameters)

    def _test__cli_temgen__treat_template_file__ok(self,
                                                   template_filepath: Path,
                                                   argv: list[str],
                                                   project_root_dir: str,
                                                   input_parameters: list):
        self._run__cli_temgen__treat_template_file__ok(template_filepath, argv, project_root_dir, input_parameters)
        self._compare_output_and_expected(project_root_dir)

    def _test__cli_temgen__treat_template_file__exception(self,
                                                          template_filepath: Path,
                                                          argv: list[str],
                                                          project_root_dir: str,
                                                          input_parameters: list):
        self._run__cli_temgen__treat_template_file__ok(template_filepath, argv, project_root_dir, input_parameters)
        self.fail()

    def _test__cli_temgen__treat_template_string__ok(self,
                                                     template_string: str,
                                                     argv: list[str],
                                                     project_root_dir: str,
                                                     input_parameters: list):
        self._run__cli_temgen__treat_template_string__ok(template_string, argv, project_root_dir, input_parameters)
        self._compare_output_and_expected(project_root_dir)

    def _test__cli_temgen__treat_template_string__exception(self,
                                                            template_string: str,
                                                            argv: list[str],
                                                            project_root_dir: str,
                                                            input_parameters: list):
        self._run__cli_temgen__treat_template_string__ok(template_string, argv, project_root_dir, input_parameters)
        self.fail()

    def _compare_file_lines_with_expected_lines(self, output_filepath: Path, expected_file_contents: str):
        expected_file_contents_lines = expected_file_contents.split('\n')
        result_file_contents_lines = self._read_output_file_contents(output_filepath).split('\n')
        for expected_var, result_var in zip(expected_file_contents_lines, result_file_contents_lines):
            self.assertEqual(expected_var, result_var)
