import base64

from statement.abstract_statement import AbstractStatement
from statement.writer.format_action import FormatAction
from statement.writer.writer import Writer


class BinaryToTextWriter(Writer):
    def __init__(self, output_stream, input_contents: bytes, statement: AbstractStatement):
        super().__init__(statement)
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
        format_actions = self._get_format_actions(FormatAction.BASE64)
        for format_action in format_actions:
            match format_action:
                case FormatAction.BASE64:
                    return base64.standard_b64encode(self.__input_contents).decode("ascii")
                case FormatAction.BASE64_URL:
                    return base64.urlsafe_b64encode(self.__input_contents).decode("ascii")
                case _:
                    raise RuntimeError("Format action not handled when copying binary contents to text stream: "
                                       f"{format_action}.")
