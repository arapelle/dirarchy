import json
from functools import singledispatchmethod


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

    @singledispatchmethod
    def update_vars_from_dict(self, var_dict: list[(str, str)]):
        self.update(var_dict)
        for key, value in var_dict:
            self.__log_set_var(key, value)

    @update_vars_from_dict.register
    def _(self, var_dict: dict):
        self.update(var_dict)
        for key, value in var_dict.items():
            self.__log_set_var(key, value)

    def update_vars_from_files(self, var_files: list):
        for var_file in var_files:
            with open(var_file) as vars_file:
                var_dict = json.load(vars_file)
                if not isinstance(var_dict, dict):
                    raise Exception(f"The variables file '{var_file}' does not contain a valid JSON dict.")
                for key, value in var_dict.items():
                    self[key] = value
                    self.__log_set_var(key, value)

    def __log_set_var(self, var_name, var_value):
        var_value_log_str = str(var_value)
        limit = 1024
        if len(var_value_log_str) > limit:
            var_value_log_str = var_value_log_str[:limit] + "..."
        self.__logger.info(f"Set var: {var_name} = '{var_value_log_str}'")

