# The thief has found himself a new place for his thievery again.
# There is only one entrance to this area, called the "root." Besides the root,
# each house has one and only one parent house. After a tour, the smart thief realized that "all houses in this place
# forms a binary tree". It will automatically contact the police if two directly-linked houses were broken into on
# the same night.
#
# Determine the maximum amount of money the thief can rob tonight without alerting the police.

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def rob(root: TreeNode) -> int:
    # we need the max left and the max right

    if root:

        rob(root.left)

        print(root.val)
        if max_left < root.val:
            max_left = root.val
            print(f'{max_left} is the max')

        rob(root.right)
        print(root.val)
        if max_left < root.val:
            max_left = root.val
            print(f'{max_left} is the max')

    return max_left
