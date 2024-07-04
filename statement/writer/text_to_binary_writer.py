import base64
import locale

from statement.abstract_statement import AbstractStatement
from statement.writer.format_action import FormatAction
from statement.writer.strip_action import apply_strip, StripAction
from statement.writer.writer import Writer


class TextToBinaryWriter(Writer):
    def __init__(self, output_stream, input_contents: str, input_encoding, statement: AbstractStatement):
        super().__init__(statement)
        self.__output_stream = output_stream
        self.__input_contents = input_contents
        self.__input_encoding = input_encoding if input_encoding is not None else locale.getencoding()

    def execute(self):
        format_actions = self._get_format_actions(FormatAction.FORMAT)
        format_actions_are_base64 = FormatAction.BASE64 in format_actions or FormatAction.BASE64_URL in format_actions
        default_strip_attr = StripAction.STRIP if format_actions_are_base64 else StripAction.STRIP_HS
        strip_attr = self.statement.current_node().get("strip", default_strip_attr)
        strip_action = StripAction(self.statement.vformat(strip_attr))
        self.__input_contents = apply_strip(self.__input_contents, strip_action)
        for format_action in format_actions:
            self.__input_contents = self.__apply_format(format_action)
        self.__output_stream.write(self.__input_contents)

    def __apply_format(self, format_action: FormatAction):
        match format_action:
            case FormatAction.RAW:
                return bytes(self.__input_contents, self.__input_encoding)
            case FormatAction.FORMAT:
                return bytes(self.statement.vformat(self.__input_contents), self.__input_encoding)
            case FormatAction.BASE64:
                return base64.standard_b64decode(self.__input_contents)
            case FormatAction.BASE64_URL:
                return base64.urlsafe_b64decode(self.__input_contents)
            case _:
                raise RuntimeError(f"Format action not handled when copying text to binary stream: {format_action}.")
