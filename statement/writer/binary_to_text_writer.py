import base64

from statement.abstract_statement import AbstractStatement
from statement.writer.format_action import FormatAction


class BinaryToTextWriter:
    def __init__(self, output_stream, input_contents: bytes, statement: AbstractStatement):
        self.__output_stream = output_stream
        self.__input_contents = input_contents
        self.__statement = statement

    def execute(self):
        self.__input_contents = self.__apply_strip()
        self.__input_contents = self.__apply_format()
        self.__output_stream.write(self.__input_contents)

    def __apply_strip(self):
        if "strip" in self.__statement.current_node().attrib:
            raise RuntimeError("Strip is not available when copying binary contents to text stream.")
        return self.__input_contents

    def __apply_format(self):
        default_format_attr = FormatAction.BASE64
        format_attr = self.__statement.current_node().get("format", default_format_attr)
        format_action = FormatAction(self.__statement.format_str(format_attr))
        match format_action:
            case FormatAction.BASE64:
                return base64.standard_b64encode(self.__input_contents).decode("ascii")
            case FormatAction.BASE64_URL:
                return base64.urlsafe_b64encode(self.__input_contents).decode("ascii")
            case _:
                raise RuntimeError("Format action not handled when copying binary contents to text stream: "
                                   f"{format_action}.")
