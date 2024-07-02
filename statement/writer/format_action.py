from enum import StrEnum
from statement.abstract_statement import AbstractStatement


class FormatAction(StrEnum):
    RAW = "raw"
    FORMAT = "format"
    BASE64 = "base64"
    BASE64_URL = "base64-url"
