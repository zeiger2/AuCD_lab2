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
    def __init__(self):
        self.root = None
    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return TreeNode(key)
        elif key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        balance = self.get_balance(node)

        # Левый левый случай
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Правый правый случай
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Левый правый случай
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Правый левый случай
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def delete(self, key):
        self.root = self.delete_(self.root, key)

    def delete_(self, node, key):
        if not node:
            return node
        elif key < node.key:
            node.left = self.delete_(node.left, key)
        elif key > node.key:
            node.right = self.delete_(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self.get_min_value_node(node.right)
            node.key = temp.key
            node.right = self.delete_(node.right, temp.key)

        if node is None:
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        balance = self.get_balance(node)

        # Левый левый случай
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        # Левый правый случай
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Правый правый случай
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        # Правый левый случай
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self.search(node.left, key)
        return self.search(node.right, key)

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

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return (self.get_height(node.left) - self.get_height(node.right)) if node else 0

    def get_min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self.get_min_value_node(node.left)

    def inorder(self, node):
        self._inorder_rec(node)

    def _inorder_rec(self, node):
        if node is not None:
            self._inorder_rec(node.left)
            print(node.key, end=' ')
            self._inorder_rec(node.right)

    def print_tree(self, node, level=0, prefix="Root:"):
        if node is not None:
            print(" " * (level * 4) + prefix + " " + str(node.key))
            self.print_tree(node.left, level + 1, prefix="L---")
            self.print_tree(node.right, level + 1, prefix="R---")
            

    def level_width(self):
        if self.root is None:
            print("Tree is empty.")
            return

        queue = [self.root]
        while queue:
            level_size = len(queue)
            level_width = 0
            next_level = []
            for _ in range(level_size):
                node = queue.pop(0)
                level_width += 1
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)
            print(f"Level width: {level_width}")
            queue = next_level

    def bfs(self):
        if self.root is None:
            print("Tree is empty.")
            return

        queue = [self.root]
        while queue:
            node = queue.pop(0)
            print(node.key, end=" ")
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    def display_in_ordered(self, node=None):
        if node is None:
            return 
        if node:
            self.display_in_ordered(node.left)
            print(node.key, end=" ")
            self.display_in_ordered(node.right)

    def display_pre_ordered(self, node=None):
        if node is None:
            return 
        if node:
            print(node.key, end=" ")
            self.display_pre_ordered(node.left)
            self.display_pre_ordered(node.right)

    def display_post_ordered(self, node=None):
        if node is None:
            return 
        if node:
            self.display_post_ordered(node.left)
            self.display_post_ordered(node.right)
            print(node.key, end=" ")


avl_tree = AVLTree()

keys = [10, 20, 30, 40, 50, 25, 13, 33, 9]
for key in keys:
    avl_tree.insert(key)
print("AVL tree after inserting keys:")
avl_tree.print_tree(avl_tree.root)

avl_tree.delete(20)
print("\nAVL tree after removing 20:")
avl_tree.print_tree(avl_tree.root)

result = avl_tree.search(avl_tree.root, 25)
if result:
    print("\nItem 25 found.")
else:
    print("\nItem 25 not found.")
result = avl_tree.search(avl_tree.root, 20)
if result:
    print("\nItem 20 found.")
else:
    print("\nItem 20 not found.")

print("\nWide crawl:")
avl_tree.bfs()

print("\nDepth First Traversal Pre Ordered (Rlr):")
avl_tree.display_pre_ordered(avl_tree.root)

print("\nDepth First Traversal In Ordered (lRr):")
avl_tree.display_in_ordered(avl_tree.root)

print("\nDepth First Traversal Post Ordered (lrR):")
avl_tree.display_post_ordered(avl_tree.root)

print('\n')




# def experiment(num_insertions):
#     avl = AVLTree()
#     root=None
#     heights = []

#     for key in range(1, num_insertions + 1):
#         root = avl.insert(root, key)
#         heights.append(avl.get_height(root))

#     return heights

# max_insertions = 1000
# heights = experiment(max_insertions)

# x_values = list(range(1, max_insertions + 1))

# plt.figure(figsize=(10, 6))
# plt.plot(x_values, heights, label='Tree height (measured)', color='blue')

# # plt.plot(x_values, [((np.log2(np.sqrt(5)*(x+1)))/(np.log2((1+np.sqrt(5))/2))-1) for x in x_values], label='Theoretical high height ', color='orange', linestyle='--')
# # plt.plot(x_values, [(np.log2(x)) for x in x_values], label='Theoretical height O(log(n))', color='red', linestyle='--')

# plt.plot(x_values, [ceil((np.log2(np.sqrt(5)*(x+1)))/(np.log2((1+np.sqrt(5))/2))-1) for x in x_values], label='Theoretical high height ', color='orange', linestyle='--')
# plt.plot(x_values, [ceil(np.log2(x)) for x in x_values], label='Theoretical height O(log(n))', color='red', linestyle='--')

# plt.title('Dependence of the height of the AVL tree on the number of keys')
# plt.xlabel('Number of keys n')
# plt.ylabel('Tree height h(n)')
# plt.legend()
# plt.grid()
# plt.show()