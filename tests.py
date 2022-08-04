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

    def test_delitem(self):
        def fuck(ind):
            def wrapper():
                del self.s[ind]

            return wrapper

        # Return TypeError for not integer index
        self.assertRaises(TypeError, fuck('asdasd'))
        self.assertRaises(TypeError, fuck(12.4))
        self.assertRaises(TypeError, fuck((2, )))

        # Стандартные процедуры удаления
        self.s.push_range(range(0, 10))
        lst = list(reversed(range(0, 10)))
        self.assertRaises(IndexError, fuck(200))
        self.assertRaises(IndexError, fuck(10))
        for ind in [0, 4, 2, 0]:
            del self.s[ind]
            del lst[ind]
            self.assertEqual(lst, list(self.s))

        # Удаление первого элемента из пустого стека
        self.s.clear()
        self.assertRaises(IndexError, fuck(0))

        # Удаление последнего элемента из стека
        self.s.push(1)
        del self.s[0]
        self.assertEqual([], list(self.s))

    def test_sum(self):
        ran = range(1, 10)
        self.s.push_range(ran)
        self.assertEqual(sum(ran), sum(self.s))

    def test_set(self):
        self.s.push_range(range(10))
        self.s[1] = 100
        lst = list((range(10)))
        lst[-2] = 100
        self.assertListEqual(list(reversed(self.s)), lst)

    def tearDown(self) -> None:
        del self.s


if __name__ == "__main__":
    unittest.main()
