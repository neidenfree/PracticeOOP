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
            print(list(reversed(self.s)), list(ran))
            reversed(self.s)
            self.assertListEqual(list(reversed(self.s)), list(ran))

    def tearDown(self) -> None:
        del self.s


if __name__ == "__main__":
    unittest.main()
