import unittest
from stack import Stack, Queue, Deque


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
        self.assertRaises(TypeError, fuck((2,)))

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

    def test_clear(self):
        sz = self.s.__sizeof__()
        self.s.push_range(range(20))
        self.s.clear()
        self.assertEqual(sz, self.s.__sizeof__())

    def tearDown(self) -> None:
        del self.s


class TestQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.q = Queue()

    def test_push(self) -> None:
        self.assertListEqual(list(self.q), [])
        self.q.push(1)
        self.assertListEqual(list(self.q), [1])
        self.q.push(2)
        self.assertListEqual(list(self.q), [1, 2])
        self.q.push(3)
        self.assertListEqual(list(self.q), [1, 2, 3])

    def test_push_range(self) -> None:
        self.assertEqual(list(self.q), [])
        self.q.push_range(range(1, 10))
        self.assertEqual([*range(1, 10)], list(self.q))

    def test_set_item(self):
        self.q.push_range(range(0, 10))
        self.q[0] = 100
        lst = list(range(0, 10))
        lst[0] = 100
        self.assertListEqual(lst, list(self.q))

    def tearDown(self) -> None:
        del self.q


class TestDeque(unittest.TestCase):
    def setUp(self) -> None:
        self.d = Deque()

    def test_push_front(self):
        self.d.push_front(2)
        self.assertEqual(2, self.d.tail.data)
        self.assertEqual(2, self.d.head.data)
        self.d.push_front(1)
        self.assertEqual(2, self.d.tail.data)
        self.assertEqual(1, self.d.head.data)

    def test_push_back(self):
        self.d.push_back(2)
        self.assertEqual(2, self.d.tail.data)
        self.assertEqual(2, self.d.head.data)
        self.d.push_back(1)
        self.assertEqual(1, self.d.tail.data)
        self.assertEqual(2, self.d.head.data)

    def test_iter(self):
        self.d.push_front(1)
        self.d.push_front(2)
        self.d.push_front(3)
        self.d.push_front(4)
        it = iter(self.d)
        z = next(it)
        self.assertEqual(z, 1)
        z = next(it)
        self.assertEqual(z, 2)
        z = next(it)
        self.assertEqual(z, 3)

    def test_push_front_back_range(self):
        self.d.push_front_range(range(5))
        self.assertEqual(list(self.d), [*range(5)])
        lst = list(reversed(range(10, 15)))
        lst.extend(list(range(5)))
        self.d.push_back_range(range(10, 15))
        self.assertListEqual(list(self.d), lst)

    def test_reversed(self):
        self.d.push_front_range(range(5))
        reversed(self.d)
        d_lst = list(self.d)
        lst = list(reversed(range(5)))
        self.assertEqual(d_lst, lst)

        self.d.clear()
        # self.d.push_front(5)
        reversed(self.d)
        self.assertEqual(self.d.tail, None)

    def test_getitem(self):
        def func(index):
            def wrapper(*args, **kwargs):
                return self.d[index]

            return wrapper

        self.d.push_front_range(range(10))
        lst = list(range(10))
        self.assertEqual(self.d[9], lst[9])
        self.assertRaises(TypeError, func(2.4))
        self.assertRaises(IndexError, func(10))
        self.assertRaises(IndexError, func(-1))
        for i in range(10):
            self.assertEqual(self.d[i], lst[i])
        
    def tearDown(self) -> None:
        del self.d


if __name__ == "__main__":
    unittest.main()
