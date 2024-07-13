import unittest
from unittest import TestCase

from ui.basic.string_check import GraphicStringCheck, IntStringCheck, UintStringCheck, FloatStringCheck, \
    BoolStringCheck, FullmatchStringCheck, MatchStringCheck


class TestStringCheck(TestCase):
    def test__graphic_string_check__valid_entry__ok(self):
        str_check = GraphicStringCheck()
        valid, error_msg = str_check.check("598dza dzaA dE")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)
        valid, error_msg = str_check.check("  . 598dza dzaA dE  ")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)

    def test__graphic_string_check__invalid_entry__err(self):
        str_check = GraphicStringCheck()
        valid, error_msg = str_check.check("")
        self.assertFalse(valid)
        self.assertEqual("INVALID ENTRY: ''\nExpecting a value of type gstr.", error_msg)

    def test__int_string_check__valid_entry__ok(self):
        str_check = IntStringCheck()
        valid, error_msg = str_check.check("598")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)
        valid, error_msg = str_check.check("  598  ")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)

    def test__int_string_check__invalid_entry__err(self):
        str_check = IntStringCheck()
        entry = "  -598.  "
        valid, error_msg = str_check.check(entry)
        self.assertFalse(valid)
        self.assertEqual(f"INVALID ENTRY: '{entry}'\nExpecting a value of type int, regex: -?\\d+", error_msg)

    def test__uint_string_check__valid_entry__ok(self):
        str_check = UintStringCheck()
        valid, error_msg = str_check.check("598")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)
        valid, error_msg = str_check.check("  598  ")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)

    def test__uint_string_check__invalid_entry__err(self):
        str_check = UintStringCheck()
        entry = "  -598  "
        valid, error_msg = str_check.check(entry)
        self.assertFalse(valid)
        self.assertEqual(f"INVALID ENTRY: '{entry}'\nExpecting a value of type uint, regex: \\d+", error_msg)

    def test__float_string_check__valid_entry__ok(self):
        str_check = FloatStringCheck()
        valid, error_msg = str_check.check("598")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)
        valid, error_msg = str_check.check("  598.45  ")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)
        valid, error_msg = str_check.check("-598")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)
        valid, error_msg = str_check.check("-598.25")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)

    def test__float_string_check__invalid_entry__err(self):
        str_check = FloatStringCheck()
        entry = "-598.25a"
        valid, error_msg = str_check.check(entry)
        self.assertFalse(valid)
        self.assertEqual(f"INVALID ENTRY: '{entry}'\nExpecting a value of type float, regex: -?\\d+(\\.\\d+)?",
                         error_msg)

    def test__bool_string_check__valid_entry__ok(self):
        str_check = BoolStringCheck()
        valid, error_msg = str_check.check("true")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)
        valid, error_msg = str_check.check("false")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)
        valid, error_msg = str_check.check("True")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)
        valid, error_msg = str_check.check("False")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)

    def test__bool_string_check__invalid_entry__err(self):
        str_check = BoolStringCheck()
        entry = "1"
        valid, error_msg = str_check.check(entry)
        self.assertFalse(valid)
        self.assertEqual(f"INVALID ENTRY: '{entry}'\nExpecting a value of type bool, regex: [tT]rue|[fF]alse",
                         error_msg)

    def test__fullmatch_string_check__valid_entry__ok(self):
        str_check = FullmatchStringCheck(regex=r"([bctgk][aeiou])+")
        valid, error_msg = str_check.check("baka")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)
        valid, error_msg = str_check.check("  baka  ")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)

    def test__fullmatch_string_check__invalid_entry__err(self):
        str_check = FullmatchStringCheck(regex=r"([bctgk][aeiou])+")
        entry = "bakaNA"
        valid, error_msg = str_check.check(entry)
        self.assertFalse(valid)
        self.assertEqual(f"INVALID ENTRY: '{entry}'\nExpecting a value satisfying the regex: ([bctgk][aeiou])+",
                         error_msg)
        str_check = FullmatchStringCheck(regex=r"([bctgk][aeiou])+", strip=False)
        entry = "  baka  "
        valid, error_msg = str_check.check(entry)
        self.assertFalse(valid)
        self.assertEqual(f"INVALID ENTRY: '{entry}'\nExpecting a value satisfying the regex: ([bctgk][aeiou])+",
                         error_msg)

    def test__match_string_check__valid_entry__ok(self):
        str_check = MatchStringCheck(regex=r"([bctgk][aeiou])+")
        valid, error_msg = str_check.check("baka")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)
        valid, error_msg = str_check.check("bakaNA")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)

    def test__match_string_check__invalid_entry__err(self):
        str_check = MatchStringCheck(regex=r"([bctgk][aeiou])+")
        entry = "b.ka"
        valid, error_msg = str_check.check(entry)
        self.assertFalse(valid)
        self.assertEqual(f"INVALID ENTRY: '{entry}'\nExpecting a value satisfying the regex: ([bctgk][aeiou])+",
                         error_msg)

    def test__even_uint_string_check__valid_entry__ok(self):
        str_check = UintStringCheck()
        str_check.next = FullmatchStringCheck(regex=r".*[02468]")
        valid, error_msg = str_check.check("142")
        self.assertTrue(valid)
        self.assertEqual("", error_msg)

    def test__even_uint_string_check__invalid_entry__err(self):
        str_check = UintStringCheck()
        str_check.next = FullmatchStringCheck(regex=r".*[02468]")
        entry = "-142"
        valid, error_msg = str_check.check(entry)
        self.assertFalse(valid)
        self.assertEqual(f"INVALID ENTRY: '{entry}'\nExpecting a value of type uint, regex: \\d+",
                         error_msg)
        entry = "1427"
        valid, error_msg = str_check.check(entry)
        self.assertFalse(valid)
        self.assertEqual(f"INVALID ENTRY: '{entry}'\nExpecting a value satisfying the regex: .*[02468]",
                         error_msg)


if __name__ == '__main__':
    unittest.main()
