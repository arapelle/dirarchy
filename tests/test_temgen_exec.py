import platform
import subprocess
import unittest

from tests.test_temgen_base import TestTemgenBase


class TestTemgenExec(TestTemgenBase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._local_sub_dirpath = "temgen/exec"
        super().setUpClass()

    def test__exec_python__raw__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <exec lang="python">
with open("data.txt", "w") as data_file:
    for i in range(5):
        data_file.write(f"{i}\\n")
    data_file.write("{fruit}\\n")
        </exec>
    </dir>
</template>
        """
        project_root_dir = "exec_python__raw"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__exec_python__format__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <exec lang="python" format="format">
with open("data.txt", "w") as data_file:
    for i in range(5):
        data_file.write(f"{{i}}\\n")
    data_file.write("{$OUTPUT_DIR}\\n")
        </exec>
    </dir>
</template>
        """
        project_root_dir = "exec_python__format"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    @unittest.skipIf(platform.system().strip().lower() == "windows", "Linux env unit test only.")
    def test__exec_sh__raw__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <exec lang="sh">
for i in {1..5}
do
    echo $i &gt;&gt; data.txt
done
echo "{fruit}" &gt;&gt; data.txt
        </exec>
    </dir>
</template>
        """
        project_root_dir = "exec_sh__raw"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    @unittest.skipIf(platform.system().strip().lower() == "windows", "Linux env unit test only.")
    def test__exec_bash__format__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <exec lang="bash" format="format">
for i in {{1..5}}
do
    echo $i &gt;&gt; data.txt
done
echo "{$OUTPUT_DIR}" &gt;&gt; data.txt
        </exec>
    </dir>
</template>
        """
        project_root_dir = "exec_bash__format"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__exec_python__timeout_not_expired__ok(self):
        template_string = """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{project_root_dir}">
        <exec lang="python" timeout="0.2">
import time
time.sleep(0.05)
with open("data.txt", "w") as data_file:
    data_file.write("Just in time!")
        </exec>
    </dir>
</template>
        """
        project_root_dir = "exec_python__timeout_not_expired"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    @staticmethod
    def __exec_python_timeout_expired_string(exec_attrs=""):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
    </vars>
    <dir path="{{project_root_dir}}">
        <exec lang="python" timeout="0.05" {exec_attrs}>
import time
with open("data.txt", "w") as data_file:
    data_file.write("start\\n")
    data_file.flush()
    time.sleep(0.06)
    data_file.write("end\\n")
    data_file.flush()
        </exec>
    </dir>
</template>
        """

    def test__exec_python__timeout_expired_error__exception(self):
        template_string = self.__exec_python_timeout_expired_string()
        project_root_dir = "exec_python__timeout_expired_error"
        input_parameters = []
        with self.assertRaises(subprocess.TimeoutExpired):
            self._test__treat_template_xml_string__exception(template_string, project_root_dir, input_parameters)

    def test__exec_python__timeout_expired_warning__exception(self):
        template_string = self.__exec_python_timeout_expired_string('on-timeout="WARNING"')
        project_root_dir = "exec_python__timeout_expired_warning"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__exec_python__timeout_expired_ok__exception(self):
        template_string = self.__exec_python_timeout_expired_string('on-timeout="OK"')
        project_root_dir = "exec_python__timeout_expired_ok"
        input_parameters = []
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__exec_python__calls_template__ok(self):
        main_template_string = self.__exec_python__main_template_str()
        sub_template_filepath = self._make_sub_template_filepath("sub_exec_template")
        sub_template_string = self.__exec_python__sub_template_str()
        project_root_dir = "exec_python__calls_template"
        input_parameters = [str(sub_template_filepath)]
        self._test__treat_template_xml_string_calling_template__ok(main_template_string,
                                                                   sub_template_filepath,
                                                                   sub_template_string,
                                                                   project_root_dir,
                                                                   input_parameters)

    @staticmethod
    def __exec_python__main_template_str():
        return """<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="template_path" type="gstr" />
    </vars>
    <dir path="{project_root_dir}">
        <exec template="{template_path}" />
    </dir>
</template>
        """

    @staticmethod
    def __exec_python__sub_template_str():
        return """<?xml version="1.0"?>
<template>
    <exec lang="python">
with open("data.txt", "w") as data_file:
    data_file.write("Template called.\\n")
    </exec>
</template>
        """

    def __exec_python__path__string(self, exec_attrs=""):
        return f"""<?xml version="1.0"?>
<template>
    <vars>
        <var name="project_root_dir" type="gstr" regex="[a-zA-Z0-9_]+" />
        <var name="script_path" type="gstr" />
    </vars>
    <dir path="{{project_root_dir}}">
        <exec path="{{script_path}}" {exec_attrs}/>
    </dir>
</template>
        """

    def test__exec_python__path__lang_from_ext__exception(self):
        template_string = self.__exec_python__path__string()
        project_root_dir = "exec_python__path__lang_from_ext"
        input_parameters = ["{$CURRENT_WORKING_DIR}/input/python/create_data.py"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__exec_python__path__lang__exception(self):
        template_string = self.__exec_python__path__string('lang="python"')
        project_root_dir = "exec_python__path__lang"
        input_parameters = ["{$CURRENT_WORKING_DIR}/input/python/create_data.py"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)

    def test__exec_python__path__format__exception(self):
        template_string = self.__exec_python__path__string('format="format"')
        project_root_dir = "exec_python__path__format"
        input_parameters = ["{$CURRENT_WORKING_DIR}/input/python/fmt_create_data.py"]
        self._test__treat_template_xml_string__ok(template_string, project_root_dir, input_parameters)


if __name__ == '__main__':
    unittest.main()
