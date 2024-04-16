import xml.etree.ElementTree as XMLTree
from abc import ABC

from statement.abstract_statement import AbstractStatement


class AbstractBranchStatement(AbstractStatement, ABC):
    def __init__(self, current_node: XMLTree.Element, parent_statement: AbstractStatement, **kargs):
        super().__init__(current_node, parent_statement, **kargs)
