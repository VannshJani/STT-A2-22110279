from typing import Optional, List

class Node:
    def __init__(self, val: int, left: Optional['Node'] = None, right: Optional['Node'] = None) -> None:
        self.val: int = val
        self.left: Optional['Node'] = left
        self.right: Optional['Node'] = right

def zigzag_level(root: Optional[Node]) -> List[List[int]]:
    """Return the zigzag level order traversal of a binary tree."""
    res: List[List[int]] = []
    if not root:
        return res
    level: List[Node] = [root]
    flag: int = 1
    while level:
        current: List[int] = []
        new_level: List[Node] = []
        for node in level:
            current.append(node.val)
            if node.left:
                new_level.append(node.left)
            if node.right:
                new_level.append(node.right)
        res.append(current[::flag])
        level = new_level
        flag *= -1
    return res
