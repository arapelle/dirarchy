import io
import sys
from pathlib import Path

import random_string
from ui.terminal_ui import TerminalUi
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

    def _test__treat_template_xml_string__ok(self,
                                             template_string: str,
                                             project_root_dir: str,
                                             input_parameters):
        input_parameters_str = "\n".join(input_parameters)
        sys.stdin = io.StringIO(f"{project_root_dir}\n{input_parameters_str}")
        template_generator = Temgen(TerminalUi())
        template_generator.treat_template_xml_string(template_string, output_dir=Path(self._output_dirpath))
        self._compare_output_and_expected(project_root_dir)

    def _test__treat_template_xml_string__exception(self,
                                                    template_string: str,
                                                    project_root_dir: str,
                                                    input_parameters):
        input_parameters_str = "\n".join(input_parameters)
        sys.stdin = io.StringIO(f"{project_root_dir}\n{input_parameters_str}")
        template_generator = Temgen(TerminalUi())
        template_generator.treat_template_xml_string(template_string, output_dir=Path(self._output_dirpath))
        self.fail()

    def _run__treat_template_xml_string__file_contents__ok(self,
                                                           file_contents: str,
                                                           project_root_dir: str,
                                                           input_parameters):
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
        template_generator = Temgen(TerminalUi())
        template_generator.treat_template_xml_string(template_string, output_dir=Path(self._output_dirpath))
        with open(f"{self._output_dirpath}/{project_root_dir}/data.txt") as output_file:
            return output_file.read().strip()

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

    def _run__treat_template_xml_file__ok(self,
                                          template_filepath: Path,
                                          template_string: str,
                                          project_root_dir: str,
                                          input_parameters,
                                          result_filepath=None):
        result = None
        try:
            self._make_template_file(template_filepath, template_string)
            input_parameters_str = "\n".join(input_parameters)
            sys.stdin = io.StringIO(f"{project_root_dir}\n{input_parameters_str}")
            template_generator = Temgen(TerminalUi())
            template_generator.treat_template_file(template_filepath, output_dir=Path(self._output_dirpath))
            if result_filepath is not None:
                with open(f"{self._output_dirpath}/{result_filepath}") as result_file:
                    result = result_file.read().strip()
        finally:
            template_filepath.unlink(missing_ok=True)
        return result

    def _run__treat_template_xml_file_calling_template__ok(self,
                                                           main_template_filepath: Path,
                                                           main_template_string: str,
                                                           sub_template_filepath: Path,
                                                           sub_template_string: str,
                                                           project_root_dir: str,
                                                           input_parameters,
                                                           result_filepath=None):
        result = None
        try:
            self._make_template_file(main_template_filepath, main_template_string)
            self._make_template_file(sub_template_filepath, sub_template_string)
            input_parameters_str = "\n".join(input_parameters)
            sys.stdin = io.StringIO(f"{project_root_dir}\n{input_parameters_str}")
            template_generator = Temgen(TerminalUi())
            template_generator.treat_template_file(main_template_filepath, output_dir=Path(self._output_dirpath))
            if result_filepath is not None:
                with open(f"{self._output_dirpath}/{result_filepath}") as result_file:
                    result = result_file.read().strip()
        finally:
            main_template_filepath.unlink(missing_ok=True)
            sub_template_filepath.unlink(missing_ok=True)
        return result
