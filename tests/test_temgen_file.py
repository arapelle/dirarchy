import random
import time
import unittest
from builtins import RuntimeError

from tests import config
from tests.test_temgen_base import TestTemgenBase


class TestTemgenFile(TestTemgenBase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._local_sub_dirpath = "temgen/file"
        super().setUpClass()

    def test__text_to_text_file__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="element" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt" strip="lstrip">
element: {element}
        </file>
    </dir>
</template>
            """
        project_root_dir = "text_to_text_file"
        input_parameters = ["fire"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__text_to_binary_file__base64_icon__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="icon.png" encoding="binary" format="base64">
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACoElEQVRYR9WXgZExQRCFZyNABIgA
ESACZEAGRIAIyAARIAJEQAZkgAjcfVPVW7M7M3uzu1f3199VW9ya6X7z+nX3XKSU+nw//8yi/xJA
o9FQj8fjV1hLMDAej9Xn81HH41G9Xi9ngGq1qp7Pp+p0Oup2u5UGkQCwWCzUfD7XwdfrtVoul84A
5/NZHQ4HvaasOQGIU044Go0sugHa6/X0k7btdqvXsybErBRsNpvEPtjo9/sJugm83+9VrVZLrC2S
ngSAdrutrterBRwQzWYz1oUE4p0pxixmfGxYZYjDer1urSfvMCEGqOFwqHiPURmAJ2XyLncK2CBC
dG2eTCaKHGME4bv8jSgxQOUxiwFOgvgqlYrlB3agXQAAAsDT6VR/ksK8/cHZCbNYkPonOA8BEW7R
vuBtxbDQarUsFugNACQ4LHFqMzVsQKSyl9/x9X6/nY3LCwAnBEmDuFwuuv75rdvtxsFZPxgMtAZ8
OkC4aGW328VCzRxGOGUDgUz1U/+8R4B8EnC1WulKCLXZbKY7adA0FKGJMKMo0jRjNCRXR8wCAgPM
HSwIgOSVTSiekwLgdDppDYQaOmC/lG4mAGgl/1Ja5I8pKRNQSs9Vri5AnJo96SlrMfBTPsmdNB3p
huwBqNlBRfWiE994/3EYmafBKfTjFMXLyPY5D0lNDIBTIKgskx7ApUWMlDAjioLQABDU/X6Ple3L
ISJE8YjPtDIgNICs1gvtUC0XDBcAwAg7IbSbazQA8opj0iD1DaUy8Ux6fQB0SX33h7wW3AfEsVxG
XIHQQp67QK5GZAaUOZAGwWVESjSUidwM4Nh3dUtPxRAQhQDgmIpIX2D/LAVyMgQJ5bRjqkUEHHJy
WVOYAVOU9Hgs9H8BqwzzIP7ttaUZKAvoC4xKqRALWT+yAAAAAElFTkSuQmCC
        </file>
    </dir>
</template>
        """
        project_root_dir = "text_to_binary_file__base64_icon"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__text_to_binary_file__base64_data__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="bin_data" encoding="binary" format="base64">
Mu+/vR8eNe+/ve+/ve+/vQrrna/vv71h77+977+977+977+9eO+/ve+/vWDvv70l77+9Iu+/ve+/
ve+/vWjvv71m77+9Nlk/77+977+9BFQg77+9Lu+/ve+/vWkO77+9PgDvv73vv70j77+977+9GgHv
v70n77+977+9fO+/vU12b++/vVzvv71u77+9Ie+/vSU+77+977+9Mx5p77+9ARhW77+9ae+/vVQP
77+9D++/ve+/vSzvv73vv70p77+9CyNV77+977+9PShZSSpxO++/ve+/ve+/vVUR77+9byDKiO+/
vW3vv70DJt6W77+9Vl8TQSRXXmd+TXHvv70c77+9CDnvv73vv704au+/vUIQX++/vXvvv71D77+9
IANU77+9Lu+/vWkFyo8gOu+/ve+/vdeFRu+/vS1+77+977+977+9ae+/vXQM77+977+96KCN77+9
77+9MxEnMPKwuJrvv73vv73vv70T77+977+9FO+/vQHvv71W77+9Ge+/ve+/vUkC77+9GXTvv71D
77+977+977+9UNG5OiXvv70AFe+/ve+/ve+/vWvvv71177+977+9TO+/ve+/vXwF77+9Ou+/vQZA
Ve+/vQ==
        </file>
    </dir>
</template>
        """
        project_root_dir = "text_to_binary_file__base64_data"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__text_to_binary_file__base64_url_data__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="bin_data" encoding="binary" format="base64-url">
Mu-_vR8eNe-_ve-_ve-_vQrrna_vv71h77-977-977-977-9eO-_ve-_vWDvv70l77-9Iu-_ve-_
ve-_vWjvv71m77-9Nlk_77-977-9BFQg77-9Lu-_ve-_vWkO77-9PgDvv73vv70j77-977-9GgHv
v70n77-977-9fO-_vU12b--_vVzvv71u77-9Ie-_vSU-77-977-9Mx5p77-9ARhW77-9ae-_vVQP
77-9D--_ve-_vSzvv73vv70p77-9CyNV77-977-9PShZSSpxO--_ve-_ve-_vVUR77-9byDKiO-_
vW3vv70DJt6W77-9Vl8TQSRXXmd-TXHvv70c77-9CDnvv73vv704au-_vUIQX--_vXvvv71D77-9
IANU77-9Lu-_vWkFyo8gOu-_ve-_vdeFRu-_vS1-77-977-977-9ae-_vXQM77-977-96KCN77-9
77-9MxEnMPKwuJrvv73vv73vv70T77-977-9FO-_vQHvv71W77-9Ge-_ve-_vUkC77-9GXTvv71D
77-977-977-9UNG5OiXvv70AFe-_ve-_ve-_vWvvv71177-977-9TO-_ve-_vXwF77-9Ou-_vQZA
Ve-_vQ==
        </file>
    </dir>
</template>
        """
        project_root_dir = "text_to_binary_file__base64_url_data"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    @staticmethod
    def __copy_text_file_to_text_file__format__str(copy_format_attr: str):
        return f"""<?xml version="1.0"?>
    <template>
        <vars>
            <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
            <var name="fruit" value="Ananas" />
        </vars>
        <dir path="{{project_root_dir}}">
            <file path="list.txt" {copy_format_attr} copy="input/data/fruits.txt" />
        </dir>
    </template>
        """

    def test__copy_text_file_to_text_file__default_format__ok(self):
        template_string = self.__copy_text_file_to_text_file__format__str('')
        project_root_dir = "copy_text_file_to_text_file__default_format"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__copy_text_file_to_text_file__raw__ok(self):
        template_string = self.__copy_text_file_to_text_file__format__str('format="raw"')
        project_root_dir = "copy_text_file_to_text_file__raw"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__copy_text_file_to_text_file__bad_format__exception(self):
        try:
            template_string = self.__copy_text_file_to_text_file__format__str('format="base64"')
            project_root_dir = "copy_text_file_to_text_file__bad_format"
            input_parameters = []
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual(str(err), "Format action not handled when copying text to text stream: base64.")

    @staticmethod
    def __copy_binary_file_to_binary_file__format__str(copy_format_attr: str, strip_action_attr: str = ""):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="file_to_copy" type="gstr" />
    </vars>
    <dir path="{{project_root_dir}}">
        <file path="icon.png" encoding="binary" {copy_format_attr} {strip_action_attr} copy="{{file_to_copy}}" />
    </dir>
</template>
        """

    def test__copy_binary_file_to_binary_file__default_format__ok(self):
        template_string = self.__copy_binary_file_to_binary_file__format__str('')
        project_root_dir = "copy_binary_file_to_binary_file__default_format"
        input_parameters = ["input/data/butterfly.png"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__copy_binary_file_to_binary_file__raw__ok(self):
        template_string = self.__copy_binary_file_to_binary_file__format__str('format="raw"')
        project_root_dir = "copy_binary_file_to_binary_file__raw"
        input_parameters = ["input/data/butterfly.png"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__copy_binary_file_to_binary_file__bad_format__exception(self):
        try:
            template_string = self.__copy_binary_file_to_binary_file__format__str('format="base64"')
            project_root_dir = "copy_binary_file_to_binary_file__bad_format"
            input_parameters = ["input/data/butterfly.png"]
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual(str(err),
                             "Format action not handled when copying binary contents to binary stream: base64.")

    def test__copy_binary_file_to_binary_file__bad_strip__exception(self):
        try:
            template_string = self.__copy_binary_file_to_binary_file__format__str('', 'strip="strip"')
            project_root_dir = "copy_binary_file_to_binary_file__bad_strip"
            input_parameters = ["input/data/butterfly.png"]
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual(str(err),
                             "Strip is not available when copying binary contents to binary stream.")

    @staticmethod
    def __copy_binary_file_to_text_file__format__str(format_action_attr: str, strip_action_attr: str = ""):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{{project_root_dir}}">
        <file path="data.txt" {format_action_attr} {strip_action_attr} 
              copy="input/data/butterfly.png" copy-encoding="binary" />
    </dir>
</template>
        """

    def test__copy_binary_file_to_text_file__default_format__ok(self):
        template_string = self.__copy_binary_file_to_text_file__format__str('')
        project_root_dir = "copy_binary_file_to_text_file__default_format"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__copy_binary_file_to_text_file__base64__ok(self):
        template_string = self.__copy_binary_file_to_text_file__format__str('format="base64"')
        project_root_dir = "copy_binary_file_to_text_file__base64"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__copy_binary_file_to_text_file__base64_url__ok(self):
        template_string = self.__copy_binary_file_to_text_file__format__str('format="base64-url"')
        project_root_dir = "copy_binary_file_to_text_file__base64_url"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__copy_binary_file_to_text_file__bad_format__exception(self):
        try:
            template_string = self.__copy_binary_file_to_text_file__format__str('format="format"')
            project_root_dir = "copy_binary_file_to_text_file__bad_format"
            input_parameters = []
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual(str(err),
                             "Format action not handled when copying binary contents to text stream: format.")

    def test__copy_binary_file_to_text_file__bad_strip__exception(self):
        try:
            template_string = self.__copy_binary_file_to_text_file__format__str('', 'strip="strip"')
            project_root_dir = "copy_binary_file_to_text_file__bad_strip"
            input_parameters = []
            self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual(str(err),
                             "Strip is not available when copying binary contents to text stream.")

    @staticmethod
    def __copy_text_file_to_binary_file__format__str(format_action_attr: str, strip_action_attr: str = ""):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="file_to_copy" type="gstr" />
        <var name="fruit" value="Ananas" />
    </vars>
    <dir path="{{project_root_dir}}">
        <file path="bin_data" {format_action_attr} {strip_action_attr} 
              encoding="binary" copy="{{file_to_copy}}" copy-encoding="utf-8" />
    </dir>
</template>
        """

    def test__copy_text_file_to_binary_file__default_format__ok(self):
        template_string = self.__copy_text_file_to_binary_file__format__str('')
        project_root_dir = "copy_text_file_to_binary_file__default_format"
        input_parameters = ["input/data/fruits_sp.txt"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__copy_text_file_to_binary_file__format__ok(self):
        template_string = self.__copy_text_file_to_binary_file__format__str('format="format"')
        project_root_dir = "copy_text_file_to_binary_file__format"
        input_parameters = ["input/data/fruits_sp.txt"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__copy_text_file_to_binary_file__raw__ok(self):
        template_string = self.__copy_text_file_to_binary_file__format__str('format="raw"')
        project_root_dir = "copy_text_file_to_binary_file__raw"
        input_parameters = ["input/data/fruits_sp.txt"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__copy_text_file_to_binary_file__base64__ok(self):
        template_string = self.__copy_text_file_to_binary_file__format__str('format="base64"')
        project_root_dir = "copy_text_file_to_binary_file__base64"
        input_parameters = ["input/data/base64data.txt"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__copy_text_file_to_binary_file__base64_url__ok(self):
        template_string = self.__copy_text_file_to_binary_file__format__str('format="base64-url"')
        project_root_dir = "copy_text_file_to_binary_file__base64_url"
        input_parameters = ["input/data/base64urldata.txt"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__random_binary_contents__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" />
    </vars>
    <dir path="{project_root_dir}" >
        <file path="bytes.bin" encoding="binary">
            <random type="binary" min-len="4" max-len="8" />
        </file>
        <file path="abc.bin" encoding="binary">
             <random byte-set="97,98,99" min-len="2" max-len="10" />
        </file>
    </dir>
</template>
"""
        random.seed(42)
        project_root_dir = "random_binary_contents"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__format_base64_contents__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" />
        <var name="base64_data">
            <contents format="base64" copy="input/data/butterfly.png" copy-encoding="binary" />
        </var>
    </vars>
    <dir path="{project_root_dir}">
        <file path="icon.png" encoding="binary" format="format|base64">{base64_data}</file>
    </dir>
</template>
"""
        project_root_dir = "format_base64_contents"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    @staticmethod
    def __child_statement_if_str():
        return """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="var" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt" strip="strip">
            <if expr="'{var}' == 'then'">
                <then>
                    THEN
                </then>
                <else>
                    ELSE
                </else>
            </if>
        </file>
    </dir>
</template>
            """

    def test__child_statement_if__then__ok(self):
        template_string = self.__child_statement_if_str()
        project_root_dir = "child_statement_if__then"
        input_parameters = ["then"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__child_statement_if__else__ok(self):
        template_string = self.__child_statement_if_str()
        project_root_dir = "child_statement_if__else"
        input_parameters = ["else"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    @staticmethod
    def __child_statement_match_str():
        return """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="var" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt" strip="strip">
            <match expr="{var}">
                <case value="one">
                    ONE
                </case>
                <case value="two">
                    TWO
                </case>
                <case>
                    DEFAULT
                </case>
            </match>
        </file>
    </dir>
</template>
            """

    def test__child_statement_match__two__ok(self):
        template_string = self.__child_statement_match_str()
        project_root_dir = "child_statement_match__two"
        input_parameters = ["two"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__child_statement_match__default__ok(self):
        template_string = self.__child_statement_match_str()
        project_root_dir = "child_statement_match__default"
        input_parameters = ["none"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__child_statement_random__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt">
            <random type="lower_sisy" min-len="4" max-len="9" />
        </file>
    </dir>
</template>
        """
        random.seed(42)
        project_root_dir = "child_statement_random"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__child_statement_contents__text_and_copy__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="var" type="gstr" />
        <var name="fruit" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt">
            <contents>
                Hello {var}!
            </contents>
            <contents strip="strip-nl" copy="input/data/fruits_sp.txt" />
        </file>
    </dir>
</template>
        """
        project_root_dir = "child_statement_contents__text_and_copy"
        input_parameters = ["world", "Ananas"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__child_statement_contents__random__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt">
            <contents>
                <random type="lower_sisy" min-len="4" max-len="9" />
            </contents>
        </file>
    </dir>
</template>
        """
        random.seed(42)
        project_root_dir = "child_statement_contents__random"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__child_statement_contents__contents__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="fruit" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt">
            <contents>
                <contents strip="strip-nl" copy="input/data/fruits_sp.txt" />
                <contents strip="strip-nl" copy="input/data/fruits_sp.txt" />
            </contents>
        </file>
    </dir>
</template>
        """
        project_root_dir = "child_statement_contents__contents"
        input_parameters = ["Ananas"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__child_statement_if__contents__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="var" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt" strip="strip">
            <if expr="'{var}' == 'then'">
                <then>
                    <contents strip="strip-nl">THEN-CONTENTS</contents>
                </then>
                <else>
                    <contents strip="strip-nl">ELSE-CONTENTS</contents>
                </else>
            </if>
        </file>
    </dir>
</template>
        """
        project_root_dir = "child_statement_if__contents"
        input_parameters = ["then"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__child_statement_match__contents__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="var" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <file path="data.txt" strip="strip">
            <match expr="{var}">
                <case value="one">
                    <contents strip="strip-nl">ONE-CONTENTS</contents>
                </case>
                <case>
                    <contents strip="strip-nl">DEFAULT-CONTENTS</contents>
                </case>
            </match>
        </file>
    </dir>
</template>
        """
        project_root_dir = "child_statement_match__contents"
        input_parameters = ["one"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__file_calls_template__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="templates_dir" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <file template="{templates_dir}/temfile" template-version="1">
EOF
        </file>
    </dir>
</template>
        """
        project_root_dir = "file_calls_template"
        templates_dir = config.local_templates_dirpath()
        input_parameters = [f"{templates_dir}", "stuff", "card"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    @staticmethod
    def __contents_calls_template__main_template_str(contents_attrs=""):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="template_path" type="gstr" />
    </vars>
    <dir path="{{project_root_dir}}">
        <file path="data.txt">
            <contents template="{{template_path}}" {contents_attrs}>
                <contents>
- Indeed.
                </contents>
            </contents>
        </file>
    </dir>
</template>
        """

    @staticmethod
    def __contents_calls_template__sub_template_str():
        return """<?xml version="1.0"?>
<template>
    <contents>
- Wonderful text, isn't it ?
    </contents>
</template>
        """

    def test__contents_calls_template__ok(self):
        main_template_string = self.__contents_calls_template__main_template_str()
        sub_template_filepath = self._make_sub_template_filepath("contents_file_template")
        sub_template_string = self.__contents_calls_template__sub_template_str()
        project_root_dir = "contents_calls_template"
        input_parameters = [str(sub_template_filepath)]
        self._test__treat_template_xml_string_calling_template__ok(main_template_string,
                                                                   sub_template_filepath,
                                                                   sub_template_string,
                                                                   project_root_dir,
                                                                   input_parameters)

    def test__contents_calls_template__exception(self):
        main_template_string = self.__contents_calls_template__main_template_str('strip="strip"')
        sub_template_filepath = self._make_sub_template_filepath("contents_file_template")
        sub_template_string = self.__contents_calls_template__sub_template_str()
        project_root_dir = "contents_calls_template"
        input_parameters = [str(sub_template_filepath)]
        try:
            self._test__treat_template_xml_string_calling_template__exception(main_template_string,
                                                                              sub_template_filepath,
                                                                              sub_template_string,
                                                                              project_root_dir,
                                                                              input_parameters)
        except RuntimeError as err:
            self.assertEqual("Unexpected attribute when calling 'contents' template: strip.", str(err))

    def test__contents_template_alone__exception(self):
        template_string = """<?xml version="1.0"?>
<template>
    <contents>TEXT</contents>
</template>
            """
        project_root_dir = "text_to_text_file"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'template', bad child node type: contents.", str(err))

    def test__random_vars__exception(self):
        # random, vars -> exception
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <file path="{project_root_dir}/data.txt">
         <random type="lower_sisy" len="7">
            <vars />
         </random>
    </file>
</template>
            """
        project_root_dir = "random_vars"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'random', bad child node type: vars.", str(err))

    def test__random_var__exception(self):
        # random, var -> exception
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <file path="{project_root_dir}/data.txt">
         <random type="lower_sisy" len="7">
            <var />
         </random>
    </file>
</template>
            """
        project_root_dir = "random_var"
        input_parameters = []
        try:
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'random', bad child node type: var.", str(err))

    def test__file_calls_template__template_raises_exception__exception(self):
        main_template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="sub_template" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <file template="{sub_template}">
END
        </file>
    </dir>
</template>
        """
        sub_template_filepath = self._make_sub_template_filepath("sub_template")
        sub_template_string = """<?xml version="1.0"?>
<template>
    <file path="data.txt">
        <random type="lower_sisy" len="4">
            <vars />
        </random>
    </file>
</template>
        """
        project_root_dir = "file_calls_template__template_raises_exception"
        input_parameters = [str(sub_template_filepath)]
        try:
            self._test__treat_template_xml_string_calling_template__exception(main_template_string,
                                                                              sub_template_filepath,
                                                                              sub_template_string,
                                                                              project_root_dir,
                                                                              input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'random', bad child node type: vars.", str(err))

    def test__file_calls_template__post_template_raises_exception__exception(self):
        main_template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="sub_template" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <file template="{sub_template}">
            <random type="lower_sisy" len="4">
                <vars />
            </random>
        </file>
    </dir>
</template>
        """
        sub_template_filepath = self._make_sub_template_filepath("sub_template")
        sub_template_string = """<?xml version="1.0"?>
<template>
    <file path="data.txt">
BEGIN
    </file>
</template>
        """
        project_root_dir = "file_calls_template__post_template_raises_exception"
        input_parameters = [str(sub_template_filepath)]
        try:
            self._test__treat_template_xml_string_calling_template__exception(main_template_string,
                                                                              sub_template_filepath,
                                                                              sub_template_string,
                                                                              project_root_dir,
                                                                              input_parameters)
        except RuntimeError as err:
            self.assertEqual("In 'random', bad child node type: vars.", str(err))


if __name__ == '__main__':
    unittest.main()
