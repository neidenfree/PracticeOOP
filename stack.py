from __future__ import annotations

from typing import Iterable

from type_utils import GeneralDescriptor, integer_type


class StackElement:
    link = GeneralDescriptor()
    data = GeneralDescriptor()

    def __init__(self, data, link: StackElement = None):
        self.data = data
        if link is None or type(link) is StackElement:
            self.link = link
        else:
            raise TypeError("Ебучий дескриптор нихуя не справился, пришлось городить такую вот хуету")


class DequeElement:
    link_prev = GeneralDescriptor()
    link_next = GeneralDescriptor()
    data = GeneralDescriptor()

    def __init__(self, data, link_prev: DequeElement = None, link_next: DequeElement = None):
        self.data = data
        if link_next is None or type(link_next) is DequeElement:
            self.link_next = link_next
        else:
            raise TypeError("Next link must be of class DequeElement!")

        if link_prev is None or type(link_prev) is DequeElement:
            self.link_prev = link_prev
        else:
            raise TypeError("Prev link must be of class DequeElement!")

    def __str__(self):
        return str(self.data)


class StackElementDescriptor(GeneralDescriptor):
    allowed_type = StackElement


class DequeElementDescriptor(GeneralDescriptor):
    allowed_type = DequeElement


class Stack:
    """My own implementation of stack data structure"""
    head = StackElementDescriptor()

    def __init__(self, head: StackElement = None):
        self._count = 0
        self.head = head

    def __len__(self):
        return self._count

    def __iter__(self):
        new_s = Stack(self.head)
        setattr(new_s, 'stop', self.head is None)
        return new_s

    def __next__(self):
        if self.stop:
            raise StopIteration
        res = self.head.data
        self.head = self.head.link
        if self.head is None:
            self.stop = True
        return res

    def __str__(self):
        if self.head is None:
            return ""
        return " => ".join([str(x) for x in self])

    def __getitem__(self, item):
        if type(item) is int:
            if item >= len(self):
                raise IndexError("Index is out of range")

            for i, el in enumerate(self):
                if i == item:
                    return el
        elif type(item) is slice:
            res = []
            indices = list(range(0, len(self)))[item]
            for i, el in enumerate(self):
                if i in indices:
                    res.append(el)
            return res
        else:
            raise TypeError("Index must be of type slice or int")

    def __delitem__(self, key):
        integer_type(key)
        if key >= self._count:
            raise IndexError
        temp = self.head
        ind = 0
        if key == 0:
            if self.head is not None:
                self.head = self.head.link
            return
        while temp is not None:
            if ind + 1 == key:
                if temp.link is not None:
                    temp.link = temp.link.link
                else:
                    temp.link = None
            temp = temp.link
            ind += 1

    def __setitem__(self, key, value):
        integer_type(key)
        if key >= self._count:
            raise IndexError
        if key == 0:
            self.head.data = value
            return
        temp = self.head
        ind = 0
        while temp is not None:
            if ind == key:
                temp.data = value
                return
            temp = temp.link
            ind += 1

    def __reversed__(self):
        if self.head is None:
            return self
        temp = self.head
        prev = None
        while temp.link is not None:
            after = temp.link
            temp.link = prev
            prev = temp
            temp = after
        temp.link = prev
        self.head = temp
        return self

    def clear(self):
        self.head = None
        self._count = 0

    def push(self, elem):
        if type(elem) == StackElement:
            # TODO: Подумать об этом получше
            se = StackElement(elem.value)
        else:
            se = StackElement(elem)
        se.link = self.head
        self.head = se
        self._count += 1

    def push_range(self, elements: Iterable):
        for elem in elements:
            self.push(elem)

    def pop(self) -> object:
        if self.head is None:
            raise IndexError("The stack is empty")
        res = self.head.data
        self.head = self.head.link
        self._count -= 1
        return res


class Queue(Stack):
    """Очередь, быстрая на доступ к элементам. Добавление элементов в очередь реализовано неоптимально."""

    def push(self, elem):
        if type(elem) == StackElement:
            sm = StackElement(elem.value)
        else:
            sm = StackElement(elem)

        if self.head is None:
            self.head = sm
            return

        temp = self.head
        while temp.link is not None:
            temp = temp.link
        temp.link = sm
        self._count += 1


class Deque:
    head = DequeElementDescriptor()
    tail = DequeElementDescriptor()

    def __init__(self, head: DequeElement = None, tail: DequeElement = None):
        self.head = head
        self.tail = tail
        self._count = 0

    def __len__(self):
        return self._count

    def __iter__(self):
        dq = Deque(self.head, self.tail)
        setattr(dq, 'stop', False)
        return dq

    def __next__(self):
        if not hasattr(self, 'stop'):
            raise AttributeError("Iterator didn't set attribute stop to this object!")
        if self.stop:
            raise StopIteration
        res = self.tail
        self.tail = self.tail.link_next
        if self.tail is None:
            self.stop = True

        return res.data

    def __str__(self):
        if self.head is None:
            return ""
        return " <=> ".join([str(x) for x in self])

    def __reversed__(self):
        if self.tail is None or self._count == 1:
            return self
        head = self.tail
        while head is not None:
            temp = head.link_prev
            head.link_prev = head.link_next
            head.link_next = temp
            head = head.link_prev
        temp = self.head
        self.head = self.tail
        self.tail = temp

        # self.head, self.tail = self.tail, self.head

    def __getitem__(self, item):
        if type(item) is slice:
            return list(self)[item]
        integer_type(item)
        if item >= len(self) or item < 0:
            raise IndexError
        if item < len(self) // 2:
            tail = self.tail
            ind = 0
            while tail is not None:
                if ind == item:
                    return tail.data
                else:
                    tail = tail.link_next
                    ind += 1
        else:
            head = self.head
            ind = len(self) - 1
            while head is not None:
                if ind == item:
                    return head.data
                else:
                    head = head.link_prev
                    ind -= 1

    def __setitem__(self, key, value):
        integer_type(key)
        if key >= len(self) or key < 0:
            raise IndexError
        if key < len(self) // 2:
            tail = self.tail
            ind = 0
            while tail is not None:
                if ind == key:
                    tail.data = value
                    return tail.data
                else:
                    tail = tail.link_next
                    ind += 1
        else:
            head = self.head
            ind = len(self) - 1
            while head is not None:
                if ind == key:
                    head.data = value
                    return
                else:
                    head = head.link_prev
                    ind -= 1


    def create_first(self, value):
        if self.head is None:
            dem = DequeElement(value)
            self.head = dem
            self.tail = dem
            self._count += 1
            return True
        return False

    def clear(self):
        self.head = None
        self.tail = None
        self._count = 0

    def push_front(self, value) -> None:
        if self.create_first(value):
            return

        dem = DequeElement(value)
        dem.link_prev = self.head
        self.head.link_next = dem
        self.head = dem
        self._count += 1

    def push_back(self, value):
        if self.create_first(value):
            return

        dem = DequeElement(value)
        dem.link_next = self.tail
        self.tail.link_prev = dem
        self.tail = dem
        self._count += 1

    def push_front_range(self, value: Iterable):
        if not isinstance(value, Iterable):
            raise TypeError(f"{value} is not Iterable!")
        for el in value:
            self.push_front(el)

    def push_back_range(self, value: Iterable):
        if not isinstance(value, Iterable):
            raise TypeError(f"{value} is not Iterable!")
        for el in value:
            self.push_back(el)
