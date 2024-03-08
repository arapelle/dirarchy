from pathlib import Path
from abc import ABC, abstractmethod

from template_tree_info import TemplateTreeInfo


class AbstractTemgen(ABC):
    @abstractmethod
    def ui(self):
        pass

    @abstractmethod
    def find_template_file(self, template_path: Path, version_attr):
        pass

    @abstractmethod
    def treat_template_tree_info(self, tree_info: TemplateTreeInfo):
        pass
