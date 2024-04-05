import base64
import locale

from statement.abstract_statement import AbstractStatement
from statement.writer.format_action import FormatAction
from statement.writer.strip_action import apply_strip, StripAction


class TextToBinaryWriter:
    def __init__(self, output_stream, input_contents: str, input_encoding, statement: AbstractStatement):
        self.__output_stream = output_stream
        self.__input_contents = input_contents
        self.__statement = statement
        self.__input_encoding = input_encoding if input_encoding is not None else locale.getencoding()

    def execute(self):
        default_format_attr = FormatAction.FORMAT
        node = self.__statement.current_node()
        format_action = FormatAction(self.__statement.format_str(node.get("format", default_format_attr)))
        format_action_is_base64 = format_action == FormatAction.BASE64 or format_action == FormatAction.BASE64_URL
        default_strip_attr = StripAction.STRIP if format_action_is_base64 else StripAction.STRIP_HS
        strip_attr = node.get("strip", default_strip_attr)
        strip_action = StripAction(self.__statement.format_str(strip_attr))
        self.__input_contents = apply_strip(self.__input_contents, strip_action)
        self.__input_contents = self.__apply_format(format_action)
        self.__output_stream.write(self.__input_contents)

    def __apply_format(self, format_action: FormatAction):
        match format_action:
            case FormatAction.RAW:
                return bytes(self.__input_contents, self.__input_encoding)
            case FormatAction.FORMAT:
                return bytes(self.__statement.format_str(self.__input_contents), self.__input_encoding)
            case FormatAction.BASE64:
                return base64.standard_b64decode(self.__input_contents)
            case FormatAction.BASE64_URL:
                return base64.urlsafe_b64decode(self.__input_contents)
            case _:
                raise RuntimeError(f"Format action not handled when copying text to binary stream: {format_action}.")
