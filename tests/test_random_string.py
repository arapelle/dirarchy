import unittest
from unittest import TestCase

import random_string


class TestRandom(TestCase):
    def test__random_string__char_set_len__ok(self):
        char_set = 'abc'
        str_len = 4
        value = random_string.random_string(char_set, str_len)
        self.assertEqual(len(value), str_len)
        for ch in value:
            self.assertIn(ch, char_set)

    def test__random_string__char_set_min_max__ok(self):
        char_set = 'a%c'
        min_len = 30
        max_len = 50
        value = random_string.random_string(char_set, min_len, max_len)
        self.assertGreaterEqual(len(value), min_len)
        self.assertLessEqual(len(value), max_len)
        for ch in value:
            self.assertIn(ch, char_set)

    def test__random_digit_string__len__ok(self):
        str_len = 4
        value = random_string.random_digit_string(str_len)
        self.assertEqual(len(value), str_len)
        for ch in value:
            self.assertIn(ch, '0123456789')

    def test__random_digit_string__min_max__ok(self):
        min_len = 30
        max_len = 50
        value = random_string.random_digit_string(min_len, max_len)
        self.assertGreaterEqual(len(value), min_len)
        self.assertLessEqual(len(value), max_len)
        for ch in value:
            self.assertIn(ch, '0123456789')

    def test__random_alpha_string__len__ok(self):
        str_len = 4
        value = random_string.random_alpha_string(str_len)
        self.assertEqual(len(value), str_len)
        for ch in value:
            self.assertIn(ch, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def test__random_alpha_string__min_max__ok(self):
        min_len = 30
        max_len = 50
        value = random_string.random_alpha_string(min_len, max_len)
        self.assertGreaterEqual(len(value), min_len)
        self.assertLessEqual(len(value), max_len)
        for ch in value:
            self.assertIn(ch, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def test__random_lower_string__len__ok(self):
        str_len = 4
        value = random_string.random_lower_string(str_len)
        self.assertEqual(len(value), str_len)
        for ch in value:
            self.assertIn(ch, 'abcdefghijklmnopqrstuvwxyz')

    def test__random_lower_string__min_max__ok(self):
        min_len = 30
        max_len = 50
        value = random_string.random_lower_string(min_len, max_len)
        self.assertGreaterEqual(len(value), min_len)
        self.assertLessEqual(len(value), max_len)
        for ch in value:
            self.assertIn(ch, 'abcdefghijklmnopqrstuvwxyz')

    def test__random_upper_string__len__ok(self):
        str_len = 4
        value = random_string.random_upper_string(str_len)
        self.assertEqual(len(value), str_len)
        for ch in value:
            self.assertIn(ch, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def test__random_upper_string__min_max__ok(self):
        min_len = 30
        max_len = 50
        value = random_string.random_upper_string(min_len, max_len)
        self.assertGreaterEqual(len(value), min_len)
        self.assertLessEqual(len(value), max_len)
        for ch in value:
            self.assertIn(ch, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def test__random_alnum_string__len__ok(self):
        str_len = 4
        value = random_string.random_alnum_string(str_len)
        self.assertEqual(len(value), str_len)
        for ch in value:
            self.assertIn(ch, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    def test__random_alnum_string__min_max__ok(self):
        min_len = 30
        max_len = 50
        value = random_string.random_alnum_string(min_len, max_len)
        self.assertGreaterEqual(len(value), min_len)
        self.assertLessEqual(len(value), max_len)
        for ch in value:
            self.assertIn(ch, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    def test__random_sisy_string__even_len__ok(self):
        consonants = 'btm'
        vowels = 'aei'
        codas = 'xk'
        str_len = 4
        value = random_string.random_sisy_string(consonants, vowels, codas, str_len)
        self.assertEqual(len(value), str_len)
        self.__check_string_is_sisy(value, consonants, vowels, codas)
        str_len = 5
        value = random_string.random_sisy_string(consonants, vowels, codas, str_len)
        self.__check_string_is_sisy(value, consonants, vowels, codas)

    def test__random_sisy_string__min_max__ok(self):
        consonants = 'btm'
        vowels = 'aei'
        codas = 'xk'
        min_len = 30
        max_len = 50
        value = random_string.random_sisy_string(consonants, vowels, codas, min_len, max_len)
        self.assertGreaterEqual(len(value), min_len)
        self.assertLessEqual(len(value), max_len)
        self.__check_string_is_sisy(value, consonants, vowels, codas)

    def __check_string_is_sisy(self, value, consonants, vowels, codas):
        for i in range(len(value) - 1):
            if i % 2 == 0:
                self.assertIn(value[i], consonants)
            else:
                self.assertIn(value[i], vowels)
        if len(value) % 2 == 1:
            self.assertIn(value[-1], codas)

    def test__random_snake_case_string__len__ok(self):
        str_len = 4
        value = random_string.random_snake_case_string(str_len)
        self.assertEqual(len(value), str_len)
        for ch in value:
            self.assertIn(ch, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
        self.assertNotEqual(value[0], '_')
        self.assertNotEqual(value[-1], '_')

    def test__random_snake_case_string__min_max__ok(self):
        min_len = 30
        max_len = 50
        value = random_string.random_snake_case_string(min_len, max_len)
        self.assertGreaterEqual(len(value), min_len)
        self.assertLessEqual(len(value), max_len)
        for ch in value:
            self.assertIn(ch, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
        self.assertNotEqual(value[0], '_')
        self.assertNotEqual(value[-1], '_')

    def test__random_format_cvqd_string__fmt_str__ok(self):
        fmt_str = '|cv_CV_qQ_dd|'
        value = random_string.random_format_cvqd_string(fmt_str)
        self.assertEqual(len(value), len(fmt_str))
        self.assertEqual(value[0], '|')
        self.assertEqual(value[-1], '|')
        self.assertIn(value[1], 'bdfgklmnprtvyz')
        self.assertIn(value[2], 'aeiou')
        self.assertEqual(value[3], '_')
        self.assertIn(value[4], 'BDFGKLMNPRTVYZ')
        self.assertIn(value[5], 'AEIOU')
        self.assertEqual(value[6], '_')
        self.assertIn(value[7], 'klrx')
        self.assertIn(value[8], 'KLRX')
        self.assertEqual(value[9], '_')
        self.assertIn(value[10], '0123456789')
        self.assertIn(value[11], '0123456789')


if __name__ == '__main__':
    unittest.main()
