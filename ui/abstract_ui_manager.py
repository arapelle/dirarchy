from abc import ABC, abstractmethod

from variables.variables_dict import VariablesDict
from variables.variables_map import VariablesMap


class AbstractUiManager(ABC):
    def __init__(self):
        self.__temgen = None

    def set_temgen(self, temgen):
        assert self.__temgen is None
        from temgen import Temgen
        assert isinstance(temgen, Temgen)
        self.__temgen = temgen

    def temgen(self):
        from temgen import Temgen
        assert isinstance(self.__temgen, Temgen)
        return self.__temgen

    @property
    def logger(self):
        return self.__temgen.logger

    @abstractmethod
    def call_ui(self, ui: str, variables: VariablesDict, variables_map: VariablesMap) -> bool:
        pass
