from __future__ import annotations

from typing import Optional, Iterable

from type_utils import GeneralDescriptor


class TreeElement:

    def __init__(self, data, left: TreeElement = None, right: TreeElement = None):
        self.data = data
        if left is None or isinstance(left, TreeElement):
            self.left = left
        else:
            raise TypeError

        if right is None or isinstance(right, TreeElement):
            self.right = right
        else:
            raise TypeError

    def __str__(self):
        return str(self.data)


class TreeElementDescriptor(GeneralDescriptor):
    allowed_type = TreeElement


class BinaryTree:
    root = TreeElementDescriptor()

    def __init__(self, root: TreeElement = None):
        self.root = root
        self.__count = 0

    def preorder_traversal(self) -> list:
        r = self.root
        res = []

        def wrapper(root: TreeElement):
            if root is None:
                return
            res.append(root.data)
            wrapper(root.left)
            wrapper(root.right)

        wrapper(r)
        return res

    def inorder_traversal(self) -> list:
        r = self.root
        res = []

        def wrapper(root: TreeElement):
            if root is None:
                return
            wrapper(root.left)
            res.append(root.data)
            wrapper(root.right)

        wrapper(r)
        return res

    def postorder_traversal(self) -> list:
        r = self.root
        res = []

        def wrapper(root: TreeElement):
            if root is None:
                return
            wrapper(root.left)
            wrapper(root.right)
            res.append(root.data)

        wrapper(r)
        return res

    def search(self, elem) -> Optional[TreeElement]:
        r = self.root
        res = None

        def helper(root: TreeElement) -> None:
            nonlocal res
            if root is None:
                return

            if root.data == elem:
                res = root
                return
            helper(root.left)
            helper(root.right)

        helper(r)

        return res


class BinarySearchTree(BinaryTree):
    def search(self, elem) -> Optional[TreeElement]:
        r = self.root
        res = None

        def helper(root: TreeElement):
            nonlocal res
            if root is None:
                return
            if root.data == elem:
                res = root
                return
            elif root.data < elem:
                helper(root.left)
            else:
                helper(root.right)

        helper(r)
        return res

    def add(self, elem):
        if self.root is None:
            self.root = TreeElement(elem)
            return

        r = self.root

        def helper(root):
            nonlocal r

            if root is None:
                root = TreeElement(elem)

            if elem < root.data:
                if root.left is None:
                    root.left = TreeElement(elem)
                    return
                else:
                    helper(root.left)
            elif elem > root.data:
                if root.right is None:
                    root.right = TreeElement(elem)
                else:
                    helper(root.right)
            else:
                return

        helper(r)

    def add_range(self, collection: Iterable):
        if not isinstance(collection, Iterable):
            raise TypeError(f"{collection} is not iterable")
        for el in collection:
            self.add(el)

    def print_tree(self):
        r = self.root

        def helper(root, spaces):
            if root is None:
                return
            helper(root.right, spaces + 5)
            print(" " * spaces, root.data)
            helper(root.left, spaces + 5)

        helper(r, 5)


