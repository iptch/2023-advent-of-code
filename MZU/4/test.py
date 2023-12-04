import unittest

import year2023_day04a as part_a
import year2023_day04b as part_b


class Test(unittest.TestCase):

    def test_part_a_with_example_data(self):
        with open('test-data-a') as file:
            lines = [line.strip() for line in file.readlines()]
            result = part_a.solve(lines, 5)
            self.assertEqual(13, result)
            print(result)

    def test_part_b_with_example_data(self):
        with open('test-data-b') as file:
            lines = [line.strip() for line in file.readlines()]
            result = part_b.solve(lines, 5)
            self.assertEqual(30, result)
            print(result)


if __name__ == '__main__':
    unittest.main()
