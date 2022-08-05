from __future__ import annotations

from typing import Optional

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


