from statement.abstract_statement import AbstractStatement
from statement.writer.format_action import FormatAction
from statement.writer.strip_action import apply_strip, StripAction
from statement.writer.writer import Writer


class TextToTextWriter(Writer):
    def __init__(self, output_stream, input_contents: str, statement: AbstractStatement):
        super().__init__(statement)
        self.__output_stream = output_stream
        self.__input_contents = input_contents
        self.__statement = statement

    def execute(self):
        default_strip_attr = StripAction.STRIP_HS
        strip_attr = self.__statement.current_node().get("strip", default_strip_attr)
        strip_action = StripAction(self.__statement.format_str(strip_attr))
        self.__input_contents = apply_strip(self.__input_contents, strip_action)
        self.__input_contents = self.__apply_format()
        self.__output_stream.write(self.__input_contents)

    def __apply_format(self):
        format_actions = self._get_format_actions(FormatAction.FORMAT)
        for format_action in format_actions:
            match format_action:
                case FormatAction.RAW:
                    return self.__input_contents
                case FormatAction.FORMAT:
                    return self.__statement.format_str(self.__input_contents)
                case _:
                    raise RuntimeError(f"Format action not handled when copying text to text stream: {format_action}.")
