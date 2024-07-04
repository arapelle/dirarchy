from statement.abstract_statement import AbstractStatement
from statement.writer.format_action import FormatAction


class Writer:
    def __init__(self, statement: AbstractStatement):
        self.__statement = statement

    @property
    def statement(self):
        return self.__statement

    def _get_format_actions(self, default_format_attr):
        node = self.statement.current_node()
        format_attr = self.statement.vformat(node.get("format", default_format_attr))
        return [FormatAction(format_action) for format_action in format_attr.split('|')]
