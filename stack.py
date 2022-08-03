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


class StackElementDescriptor(GeneralDescriptor):
    allowed_type = StackElement


class Stack:
    """My own implementation of stack data structure"""
    head = StackElementDescriptor()

    def __init__(self, head: StackElement = None):
        self.__count = 0
        self.head = head

    def __len__(self):
        return self.__count

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

    def push(self, elem):
        if type(elem) == StackElement:
            # TODO: Подумать об этом получше
            se = StackElement(elem.value)
        else:
            se = StackElement(elem)
        se.link = self.head
        self.head = se
        self.__count += 1

    def push_range(self, elements: Iterable):
        for elem in elements:
            self.push(elem)

    def pop(self) -> object:
        if self.head is None:
            raise IndexError("The stack is empty")
        res = self.head.data
        self.head = self.head.link
        self.__count -= 1
        return res
