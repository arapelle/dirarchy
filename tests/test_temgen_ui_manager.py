import unittest

from tests.test_temgen_base import TestTemgenBase
from ui.abstract_ui_manager import AbstractUiManager
from variables.variables_dict import VariablesDict
from variables.variables_map import VariablesMap


class CustomUiManager(AbstractUiManager):
    COLORS_UI_NAME = "colors"
    DARK_COLORS_UI_NAME = "dark_colors"

    def call_ui(self, ui: str, variables: VariablesDict, variables_map: VariablesMap) -> bool:
        match ui:
            case "":
                raise RuntimeError("This should not happen as empty ui must not trigger any ui call.")
            case self.COLORS_UI_NAME:
                variables.update_var_and_log("fill_color", "orange")
                variables.update_var_and_log("stroke_color", "red")
                return True
            case self.DARK_COLORS_UI_NAME:
                variables.update_var_and_log("fill_color", "dark_{fill_color}".format_map(variables_map))
                variables.update_var_and_log("stroke_color", "dark_{stroke_color}".format_map(variables_map))
                return True
            case _:
                return False


class TestTemgenUiManager(TestTemgenBase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._local_sub_dirpath = "temgen/ui_manager"
        super().setUpClass()

    @staticmethod
    def ui_manager__ui_treated__str(vars_attrs: str):
        return f"""<?xml version="1.0"?>
<template>
    <vars {vars_attrs}>
        <var name="project_root_dir" regex="[a-zA-Z0-9_]+" />
        <var name="fill_color" type="gstr" />
        <var name="stroke_color" type="gstr" />
    </vars>
    <dir path="{{project_root_dir}}">
        <file path="data.txt">
fill_color = '{{fill_color}}'
stroke_color = '{{stroke_color}}'
        </file>
        <dir path="dark">
            <vars ui="{CustomUiManager.DARK_COLORS_UI_NAME}">
                <var name="fill_color" type="gstr" />
                <var name="stroke_color" type="gstr" />
            </vars>
            <file path="data.txt">
fill_color = '{{fill_color}}'
stroke_color = '{{stroke_color}}'
            </file>
        </dir>
    </dir>
</template>
        """

    def test__vars_ui_manager__ui_treated__ok(self):
        template_string = self.ui_manager__ui_treated__str(f'ui="{CustomUiManager.COLORS_UI_NAME}"')
        project_root_dir = "vars_ui_manager__ui_treated"
        input_parameters = []
        ui_manager = CustomUiManager()
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters,
                                                  ui_manager=ui_manager)

    def test__vars_ui_manager__empty_ui__ok(self):
        template_string = self.ui_manager__ui_treated__str(f'ui=""')
        project_root_dir = "vars_ui_manager__empty_ui"
        input_parameters = ["blue", "black"]
        ui_manager = CustomUiManager()
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters,
                                                  ui_manager=ui_manager)

    def test__vars_ui_manager__ui_not_treated__ok(self):
        template_string = self.ui_manager__ui_treated__str('ui="{python} input/extra_ui/color_ui.py {output_file}"')
        project_root_dir = "vars_ui_manager__ui_not_treated"
        input_parameters = []
        ui_manager = CustomUiManager()
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters,
                                                  ui_manager=ui_manager)

    def test__vars_ui_manager__ui_not_found__exception(self):
        template_string = self.ui_manager__ui_treated__str('ui="{python} not_found.py {0} {1}"')
        project_root_dir = "vars_ui_manager__ui_not_found"
        input_parameters = []
        ui_manager = CustomUiManager()
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters,
                                                             ui_manager=ui_manager)
        except RuntimeError as err:
            self.assertTrue(str(err).find("Execution of ui did not work well") != -1)

    def test__template_ui_manager__ui_treated__ok(self):
        template_string = self.ui_manager__ui_treated__str("")
        project_root_dir = "template_ui_manager__ui_treated"
        input_parameters = []
        ui_manager = CustomUiManager()
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters,
                                                  ui_manager=ui_manager, ui=CustomUiManager.COLORS_UI_NAME)

    def test__template_ui_manager__ui_not_treated__ok(self):
        template_string = self.ui_manager__ui_treated__str('ui="{python} input/extra_ui/color_ui.py {output_file}"')
        project_root_dir = "template_ui_manager__ui_not_treated"
        input_parameters = []
        ui_manager = CustomUiManager()
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters,
                                                  ui_manager=ui_manager)


if __name__ == '__main__':
    unittest.main()
