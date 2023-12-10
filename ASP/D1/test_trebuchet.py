import unittest
from trebuchet import Trebuchet


class TestTrebuchet(unittest.TestCase):
    trebuchet = Trebuchet()

    def test_input(self):
        self.assertEqual(self.trebuchet.get_sum("test", 0), 142)
        self.assertEqual(self.trebuchet.get_sum("test2", 0), 209)
        self.assertEqual(self.trebuchet.get_sum("test", 1), 142)
        self.assertEqual(self.trebuchet.get_sum("test2", 1), 281)

    def test_get_numbers_mode_one(self):
        self.assertEqual(self.trebuchet.get_numbers("a12b3c", 0), "123")
        self.assertEqual(self.trebuchet.get_numbers("a12b", 0), "12")
        self.assertEqual(self.trebuchet.get_numbers("1ab2", 0), "12")
        self.assertEqual(self.trebuchet.get_numbers("1a2b", 0), "12")
        self.assertEqual(self.trebuchet.get_numbers("a1b2", 0), "12")
        self.assertEqual(self.trebuchet.get_numbers("ab", 0), "")
        self.assertEqual(self.trebuchet.get_numbers("one22one", 0), "22")

    def test_get_numbers_mode_two(self):
        self.assertEqual(self.trebuchet.get_numbers("one22one", 1), "1221")
        self.assertEqual(self.trebuchet.get_numbers("1one22one1", 1), "112211")
        self.assertEqual(self.trebuchet.get_numbers("1oneone22one1", 1), "1112211")
        self.assertEqual(self.trebuchet.get_numbers("1onetwo22one1", 1), "1122211")
        self.assertEqual(self.trebuchet.get_numbers("1onetwo22one1", 1), "1122211")

    def test_value_of_code(self):
        self.assertEqual(self.trebuchet.get_value_of_code("1"), 11)
        self.assertEqual(self.trebuchet.get_value_of_code("12"), 12)
        self.assertEqual(self.trebuchet.get_value_of_code("123"), 13)
        self.assertEqual(self.trebuchet.get_value_of_code("0"), 0)
        self.assertEqual(self.trebuchet.get_value_of_code("9"), 99)
        self.assertEqual(self.trebuchet.get_value_of_code("10"), 10)
        self.assertEqual(self.trebuchet.get_value_of_code("99"), 99)
        self.assertEqual(self.trebuchet.get_value_of_code("100"), 10)

    def test_code_to_value(self):
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("a123b", 0)), 13)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("a12b", 0)), 12)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("a4b", 0)), 44)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("ab", 0)), 0)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("one22one", 0)), 22)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("22one", 1)), 21)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("11two", 1)), 12)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("11three", 1)), 13)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("11four", 1)), 14)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("11five", 1)), 15)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("11six", 1)), 16)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("11seven", 1)), 17)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("11eight", 1)), 18)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("11nine", 1)), 19)
        self.assertEqual(self.trebuchet.get_value_of_code(self.trebuchet.get_numbers("22ten", 1)), 22)

    def test_replace_word_with_number(self):
        self.assertEqual(self.trebuchet.replace_word_with_number("fiveightwo"), "582")
        self.assertEqual(self.trebuchet.replace_word_with_number("fiveight"), "58")
        self.assertEqual(self.trebuchet.replace_word_with_number("1fiveightwo1"), "15821")
        self.assertEqual(self.trebuchet.replace_word_with_number("1beispiel4fiveightwort5"), "145825")



if __name__ == '__main__':
    unittest.main()
