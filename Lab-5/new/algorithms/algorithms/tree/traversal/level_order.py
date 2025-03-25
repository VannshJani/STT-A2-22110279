from typing import Optional, List

class Node:
    def __init__(self, val: int, left: Optional['Node'] = None, right: Optional['Node'] = None) -> None:
        self.val: int = val
        self.left: Optional['Node'] = left
        self.right: Optional['Node'] = right

def level_order(root: Optional[Node]) -> List[List[int]]:
    """Return the level order traversal of a binary tree."""
    ans: List[List[int]] = []
    if not root:
        return ans
    level: List[Node] = [root]
    while level:
        current: List[int] = []
        new_level: List[Node] = []
        for node in level:
            current.append(node.val)
            if node.left:
                new_level.append(node.left)
            if node.right:
                new_level.append(node.right)
        ans.append(current)
        level = new_level
    return ans
