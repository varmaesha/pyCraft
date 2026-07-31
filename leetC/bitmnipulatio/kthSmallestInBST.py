# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def kthSmallest(self, root: TreeNode, k: int) -> int:
        def inorder_traversal(node):
            if not node:
                return []

            left = inorder_traversal(node.left)
            right = inorder_traversal(node.right)

            return left + [node.val] + right

        inorder_values = inorder_traversal(root)
        return inorder_values[k - 1]

solution = Solution()
solution.kthSmallest(TreeNode(3, TreeNode(1), TreeNode(4)), 1)
solution.kthSmallest(TreeNode(5, TreeNode(3, TreeNode(2), TreeNode(4)), TreeNode(6)), 3)