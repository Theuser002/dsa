from collections import deque
from data_structures.tree_node import TreeNode
class Solution:
    def subtreeWithAllDeepest(self, root):
        if not root:
            return None

        parent = {root: None}
        q = deque([root])

        last_level = []

        while q:
            size = len(q)
            last_level = []
            for _ in range(size):
                node = q.popleft()
                last_level.append(node)

                if node.left:
                    parent[node.left] = node
                    q.append(node.left)
                if node.right:
                    parent[node.right] = node
                    q.append(node.right)
        deepest = set(last_level)

        while len(deepest) > 1:
            deepest = {parent[node] for node in deepest}

        return deepest.pop().val

sln = Solution()
print(sln.subtreeWithAllDeepest(TreeNode.list_to_tree([3,5,1,6,2,0,8,None,None,7,4,9])))