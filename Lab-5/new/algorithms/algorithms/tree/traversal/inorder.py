from typing import Optional, List

class Node:
    def __init__(self, val: int, left: Optional['Node'] = None, right: Optional['Node'] = None) -> None:
        self.val: int = val
        self.left: Optional['Node'] = left
        self.right: Optional['Node'] = right

def inorder(root: Optional[Node]) -> List[int]:
    """ In order function """
    res: List[int] = []
    if not root:
        return res
    stack: List[Node] = []
    while root or stack:
        while root:
            stack.append(root)
            root = root.left
        root = stack.pop()
        res.append(root.val)
        root = root.right
    return res

def inorder_rec(root: Optional[Node], res: Optional[List[int]] = None) -> List[int]:
    """ Recursive Implementation """
    if root is None:
        return []
    if res is None:
        res = []
    inorder_rec(root.left, res)
    res.append(root.val)
    inorder_rec(root.right, res)
    return res

if __name__ == '__main__':
    n1 = Node(100)
    n2 = Node(50)
    n3 = Node(150)
    n4 = Node(25)
    n5 = Node(75)
    n6 = Node(125)
    n7 = Node(175)
    n1.left, n1.right = n2, n3
    n2.left, n2.right = n4, n5
    n3.left, n3.right = n6, n7

    assert inorder(n1) == [25, 50, 75, 100, 125, 150, 175]
    assert inorder_rec(n1) == [25, 50, 75, 100, 125, 150, 175]
