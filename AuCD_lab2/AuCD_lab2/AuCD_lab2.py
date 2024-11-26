from math import radians
from math import ceil
import numpy as np
import matplotlib.pyplot as plt
import random

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_rec(self.root, key)

    def _insert_rec(self, root, key):
        if key < root.val:
            if root.left is None:
                root.left = Node(key)
            else:
                self._insert_rec(root.left, key)
        else:
            if root.right is None:
                root.right = Node(key)
            else:
                self._insert_rec(root.right, key)

    def search(self, key):
        return self._search_rec(self.root, key)

    def _search_rec(self, root, key):
        if root is None or root.val == key:
            return root
        if key < root.val:
            return self._search_rec(root.left, key)
        return self._search_rec(root.right, key)

    def delete(self, key):
        self.root = self._delete_rec(self.root, key)

    def _delete_rec(self, root, key):
        if root is None:
            return root

        if key < root.val:
            root.left = self._delete_rec(root.left, key)
        elif key > root.val:
            root.right = self._delete_rec(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            min_larger_node = self._min_value_node(root.right)
            root.val = min_larger_node.val
            root.right = self._delete_rec(root.right, min_larger_node.val)

        return root

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder(self):
        self._inorder_rec(self.root)

    def _inorder_rec(self, root):
        if root is not None:
            self._inorder_rec(root.left)
            print(root.val, end=' ')
            self._inorder_rec(root.right)

    def height(self):
        return self._height_rec(self.root)

    def _height_rec(self, root):
        if root is None:
            return 0
        return 1 + max(self._height_rec(root.left), self._height_rec(root.right))


# bst = BinarySearchTree()
# bst.insert(50)
# bst.insert(30)
# bst.insert(20)
# bst.insert(40)
# bst.insert(70)
# bst.insert(60)
# bst.insert(80)

# print("Input tree traversal:")
# bst.inorder()

# bst.delete(20)
# print("\nAfter removing 20:")
# bst.inorder()

# bst.delete(30)
# print("\nAfter removing 30:")
# bst.inorder()

# bst.delete(50)
# print("\nAfter removing 50:")
# bst.inorder()


# result = bst.search(40)
# if result:
#     print("\nElement 40 found.")
# else:
#     print("\nElement 40 not found.")



# def experiment(num_insertions):
#     bst = BinarySearchTree()
#     heights = []

#     for i in range(1, num_insertions + 1):
#         key = random.randint(1, 1000000) 
#         bst.insert(key)
#         heights.append(bst.height())

#     return heights

# max_insertions = 100
# heights = experiment(max_insertions)

# x_values = list(range(1, max_insertions + 1))

# plt.figure(figsize=(10, 6))
# plt.plot(x_values, heights, label='Tree height (measured)', color='blue')
# plt.plot(x_values, [ceil(np.log2(x)) for x in x_values], label='Theoretical average height O(log n)', color='orange', linestyle='--')
# plt.plot(x_values, [ceil(x) for x in x_values], label='Theoretical worst height O(n)', color='red', linestyle='--')

# plt.title('Dependence of the height of the search tree on the number of keys')
# plt.xlabel('Number of keys n')
# plt.ylabel('Tree height h(n)')
# plt.legend()
# plt.grid()
# plt.show()


def experiment(num_insertions):
    bst = BinarySearchTree()
    heights = []

    for _ in range(num_insertions):
        key = random.randint(1, 1000000) 
        bst.insert(key)
        heights.append(bst.height())

    return heights

max_insertions = 1000
heights = experiment(max_insertions)

x_values = np.array(range(1, max_insertions + 1))

log_x_values = np.log(x_values)

# Использование np.polyfit для получения коэффициентов линейной регрессии
coefficients = np.polyfit(log_x_values, heights, 1)

# Получение y = mx + b
slope = coefficients[0]
intercept = coefficients[1]

regression_heights = slope * log_x_values + intercept

step = 50
scatter_x = x_values[::step]
scatter_heights = heights[::step]

plt.scatter(scatter_x, scatter_heights, label='The height', color='blue')
plt.plot(x_values, regression_heights, color='red', label='Logarithmic regression fit')
plt.xlabel('Number of insertions')
plt.ylabel('Height of BST')
plt.title('Asymptotics of BST Height')
plt.grid()
plt.legend()
plt.show()