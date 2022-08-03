import unittest
from stack import Stack


class TestStack(unittest.TestCase):
    def setUp(self) -> None:
        self.s: Stack = Stack()

    def test_reverse(self):
        ranges = [range(1, 10), range(2, 500), range(0, 5, 2), range(0, 0),
                  range(20, 30, 3), range(20, 50, 2), range(30, 20, 1),
                  range(-10, 10), range(0)]
        for ran in ranges:
            self.s.clear()
            self.s.push_range(ran)
            self.assertListEqual(list(reversed(self.s)), list(ran))

    def test_get(self):
        self.s.push_range(range(0, 3))

        self.assertRaises(IndexError, lambda: self.s[20])
        self.assertEqual(2, self.s[0])

    def tearDown(self) -> None:
        del self.s


if __name__ == "__main__":
    unittest.main()
