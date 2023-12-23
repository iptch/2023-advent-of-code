import unittest

import year2023_day20a as part_a


class Test(unittest.TestCase):

    def test_part_a_with_example_data(self):
        with open('test-data-a1') as file:
            lines = [line.strip() for line in file.readlines()]
            result = part_a.solve(lines)
            self.assertEqual(32000000, result)
            print(result)

        with open('test-data-a2') as file:
            lines = [line.strip() for line in file.readlines()]
            result = part_a.solve(lines)
            self.assertEqual(11687500, result)
            print(result)


if __name__ == '__main__':
    unittest.main()
