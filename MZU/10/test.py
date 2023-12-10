import unittest

import year2023_day10b as part_b


class Test(unittest.TestCase):

    def test_part_b_with_example_data(self):
        with open('test-data-b') as file:
            lines = [line.strip() for line in file.readlines()]
            result = part_b.solve(lines, 'F')
            self.assertEqual(8, result)
            print(result)


if __name__ == '__main__':
    unittest.main()
