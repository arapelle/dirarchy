import unittest
from unittest import TestCase

from statement.writer.strip_action import apply_strip, StripAction


class TestApplyStrip(TestCase):
    MULTI_LINE_TEXT = """
    DATA
    """
    ONE_LINE_TEXT = "   DATA   "

    def test__apply_strip__RAW__ok(self):
        self.assertEqual(apply_strip(self.MULTI_LINE_TEXT, StripAction.RAW), self.MULTI_LINE_TEXT)

    def test__apply_strip__LSTRIP__ok(self):
        self.assertEqual(apply_strip(self.MULTI_LINE_TEXT, StripAction.LSTRIP), "DATA\n    ")

    def test__apply_strip__RSTRIP__ok(self):
        self.assertEqual(apply_strip(self.MULTI_LINE_TEXT, StripAction.RSTRIP), "\n    DATA")

    def test__apply_strip__RSTRIP_HS__ok(self):
        self.assertEqual(apply_strip(self.MULTI_LINE_TEXT, StripAction.RSTRIP_HS), "\n    DATA\n")

    def test__apply_strip__RSTRIP_NL__ok(self):
        self.assertEqual(apply_strip(self.ONE_LINE_TEXT, StripAction.RSTRIP_NL), "   DATA\n")

    def test__apply_strip__STRIP__ok(self):
        self.assertEqual(apply_strip(self.MULTI_LINE_TEXT, StripAction.STRIP), "DATA")

    def test__apply_strip__STRIP_HS__ok(self):
        self.assertEqual(apply_strip(self.MULTI_LINE_TEXT, StripAction.STRIP_HS), "DATA\n")

    def test__apply_strip__STRIP_NL__ok(self):
        self.assertEqual(apply_strip(self.ONE_LINE_TEXT, StripAction.STRIP_NL), "DATA\n")

    def test__apply_strip__bad_value__exception(self):
        try:
            apply_strip(self.ONE_LINE_TEXT, "whut")
        except ValueError as err:
            self.assertEqual(str(err), "'whut' is not a valid StripAction")


if __name__ == '__main__':
    unittest.main()
