from math import radians
from math import ceil
import numpy as np
import matplotlib.pyplot as plt
import random

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, key):
        if not root:
            return TreeNode(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        # Левый левый случай
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Правый правый случай
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Левый правый случай
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Правый левый случай
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, key):
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        if root is None:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        # Левый левый случай
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # Левый правый случай
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Правый правый случай
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # Правый левый случай
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, root, key):
        if root is None or root.key == key:
            return root
        if key < root.key:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def get_min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self.get_min_value_node(node.left)

    def inorder(self, root):
        self._inorder_rec(root)

    def _inorder_rec(self, root):
        if root is not None:
            self._inorder_rec(root.left)
            print(root.key, end=' ')
            self._inorder_rec(root.right)

    def print_tree(self, node, level=0, prefix="Root:"):
        """Function for visualizing a tree."""
        if node is not None:
            print(" " * (level * 4) + prefix + " " + str(node.key))
            self.print_tree(node.left, level + 1, prefix="L---")
            self.print_tree(node.right, level + 1, prefix="R---")

# avl_tree = AVLTree()
# root = None

# keys = [10, 20, 30, 40, 50, 25]
# for key in keys:
#     root = avl_tree.insert(root, key)
# print("AVL tree after inserting keys:")
# avl_tree.print_tree(root)

# print("\nInput tree traversal:")
# avl_tree.inorder(root)

# root = avl_tree.delete(root, 40)
# print("\nAVL tree after removing 40:")
# avl_tree.print_tree(root)

# root = avl_tree.delete(root, 20)
# print("\nAVL tree after removing 20:")
# avl_tree.print_tree(root)

# result = avl_tree.search(root, 25)
# if result:
#     print("\nItem 25 found.")
# else:
#     print("\nItem 25 not found.")

def experiment(num_insertions):
    avl = AVLTree()
    root=None
    heights = []

    for key in range(1, num_insertions + 1):
        root = avl.insert(root, key)
        heights.append(avl.get_height(root))

    return heights

max_insertions = 1000
heights = experiment(max_insertions)

x_values = list(range(1, max_insertions + 1))

plt.figure(figsize=(10, 6))
plt.plot(x_values, heights, label='Tree height (measured)', color='blue')

# plt.plot(x_values, [((np.log2(np.sqrt(5)*(x+1)))/(np.log2((1+np.sqrt(5))/2))-1) for x in x_values], label='Theoretical high height ', color='orange', linestyle='--')
# plt.plot(x_values, [(np.log2(x)) for x in x_values], label='Theoretical height O(log(n))', color='red', linestyle='--')

plt.plot(x_values, [ceil((np.log2(np.sqrt(5)*(x+1)))/(np.log2((1+np.sqrt(5))/2))-1) for x in x_values], label='Theoretical high height ', color='orange', linestyle='--')
plt.plot(x_values, [ceil(np.log2(x)) for x in x_values], label='Theoretical height O(log(n))', color='red', linestyle='--')

plt.title('Dependence of the height of the AVL tree on the number of keys')
plt.xlabel('Number of keys n')
plt.ylabel('Tree height h(n)')
plt.legend()
plt.grid()
plt.show()