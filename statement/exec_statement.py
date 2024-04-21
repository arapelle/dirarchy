import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as XMLTree
from pathlib import Path

from statement.abstract_main_statement import AbstractMainStatement
from statement.abstract_statement import AbstractStatement
from util import random_string


class ExecStatement(AbstractMainStatement):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, **kargs):
        super().__init__(current_node, parent_statement, **kargs)
        self.__lang = None
        self.__format = None
        self.__timeout = None
        self.__on_timeout = None

    def allows_template(self):
        return True

    def execute(self):
        node = self.current_node()
        self.__lang = node.get("lang", None)
        if self.__lang is not None:
            self.__lang = self.format_str(self.__lang)
        self.__format = self.format_str(node.get("format", "raw"))
        timeout_attr = node.get("timeout", None)
        if timeout_attr is not None:
            self.__timeout = float(self.format_str(timeout_attr))
        self.__on_timeout = node.get("on-timeout", "ERROR")
        script_filepath = node.attrib.get("path", None)
        if script_filepath is not None:
            self.__treat_script(script_filepath)

    def __treat_script(self, script_filepath):
        script_filepath = Path(self.format_str(script_filepath))
        if self.__lang is None:
            self.__lang = self.__resolve_executable_from_ext(script_filepath.suffix)
        match self.__format:
            case "raw":
                self.__exec_script(script_filepath)
            case "format":
                with open(script_filepath) as script_file:
                    text = script_file.read()
                    text = self.format_str(text)
                    self.__exec_script_text(text)
            case _:
                raise RuntimeError(f"Format not handled: '{self.__format}'.")

    def treat_text_of(self, node: XMLTree.Element):
        text = node.text
        if "path" in node.attrib:
            if self.is_text_empty(text):
                return
            else:
                raise RuntimeError(f"Text is not expected when 'path' attribute is provided.")
        if self.is_text_empty(text):
            raise RuntimeError(f"Text is missing or is empty in 'exec' statement.")
        text = self.__format_script_text(text)
        self.__exec_script_text(text)

    def __exec_script_text(self, text):
        script_filepath = Path(tempfile.gettempdir()) / f"tmp_{random_string.random_lower_sisy_string(8)}"
        try:
            with open(script_filepath, mode="w+") as script_file:
                script_file.write(text)
            self.__exec_script(script_filepath)
        finally:
            script_filepath.unlink(missing_ok=True)
            assert not script_filepath.exists()

    def __exec_script(self, script_filepath: Path):
        executable = self.__resolve_executable()
        cmd = [f"{executable}"] if executable is not None else []
        cmd.append(f"{script_filepath}")
        output_dirpath = self.current_dir_statement().current_output_dirpath()
        proc = subprocess.Popen(cmd, cwd=output_dirpath)
        try:
            out, err = proc.communicate(timeout=self.__timeout)
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(proc.returncode, cmd, out, err)
        except subprocess.TimeoutExpired as err:
            proc.terminate()
            try:
                proc.wait(timeout=0.1)
            except subprocess.TimeoutExpired:
                self.logger.warning(f"Process '{proc.pid}' takes time to terminate after being required to abort.")
            self.__treat_timout_expired_exception(err)

    def __format_script_text(self, text):
        match self.__format:
            case "raw":
                return text
            case "format":
                return self.format_str(text)
            case _:
                raise RuntimeError(f"Format not handled: '{self.__format}'.")

    def __resolve_executable(self):
        match self.__lang:
            case None | "batch":
                return None
            case "python":
                return sys.executable
            case "sh" | "bash" | "zsh" | "ksh" | "csh" | "tcsh" | "fish" | "ruby" | "perl" | "lua":
                return shutil.which(self.__lang)
            case _:
                raise RuntimeError(f"Code language not handled: '{self.__lang}'.")

    def __treat_timout_expired_exception(self, err: subprocess.TimeoutExpired):
        match self.__on_timeout:
            case "ERROR":
                raise err
            case "WARNING":
                self.logger.warning(f"{err}")
            case "OK":
                pass
            case _:
                raise RuntimeError(f"On-timeout action not handled: '{self.__on_timeout}'.")

    def __resolve_executable_from_ext(self, file_ext):
        match file_ext:
            case None | "" | ".exe":
                return None
            case ".py":
                return "python"
            case ".sh":
                return "bash"
            case ".rb":
                return "ruby"
            case ".pl":
                return "perl"
            case ".lua":
                return "lua"
            case _:
                self.logger.warning(f"Impossible to determine language from unknown file extension: '{file_ext}'")
                return None
