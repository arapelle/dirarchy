import json
import os
import tempfile
from pathlib import Path

from util import random_string


class VariablesDict(dict):
    def __init__(self, logger):
        super().__init__()
        self.__logger = logger

    def clone(self):
        var_dict = VariablesDict(self.__logger)
        var_dict.update(self)
        return var_dict

    def update_var_and_log(self, var_name, var_value):
        self.__log_set_var(var_name, var_value)
        self.update({var_name: var_value})

    def update_vars_from_dict(self, var_dict):
        self.update(var_dict)
        for key, value in var_dict:
            self.__log_set_var(key, value)

    def update_vars_from_files(self, var_files):
        for var_file in var_files:
            with open(var_file) as vars_file:
                var_dict = json.load(vars_file)
                if not isinstance(var_dict, dict):
                    raise Exception(f"The variables file '{var_file}' does not contain a valid JSON dict.")
                for key, value in var_dict.items():
                    self[key] = value
                    self.__log_set_var(key, value)

    def update_vars_from_extra_ui(self, cmd: str):
        from temgen import Temgen
        with tempfile.NamedTemporaryFile("w", delete=False) as vars_file:
            input_var_filepath = Path(vars_file.name)
            json.dump(self, vars_file)
        app_dirpath = Temgen.APPLICATION_DIRECTORIES.tmp_dirpath()
        output_var_filepath = app_dirpath / f"{random_string.random_lower_sisy_string(8)}.json"
        formatted_cmd = cmd.format(input_var_filepath, output_var_filepath,
                                   input_file=input_var_filepath,
                                   output_file=output_var_filepath)
        cmd_res = os.system(formatted_cmd)
        if cmd_res != 0:
            raise RuntimeError(f"Execution of custom ui did not work well (returned {cmd_res}). "
                               f"command: {formatted_cmd}")
        with open(output_var_filepath) as vars_file:
            self.update(json.load(vars_file))
        input_var_filepath.unlink(missing_ok=True)
        output_var_filepath.unlink(missing_ok=True)

    def __log_set_var(self, var_name, var_value):
        var_value_log_str = str(var_value)
        limit = 1024
        if len(var_value_log_str) > limit:
            var_value_log_str = var_value_log_str[:limit] + "..."
        self.__logger.info(f"Set var: {var_name} = '{var_value_log_str}'")

