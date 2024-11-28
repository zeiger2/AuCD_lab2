from math import radians
from math import ceil
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
import random

class Node:
    def __init__(self, data, color="red", left=None, right=None, parent=None):
        self.data = data
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent

class RedBlackTree:
    def __init__(self):
        self.NIL_LEAF = Node(data=None, color="black")
        self.root = self.NIL_LEAF

    def insert(self, data):
        new_node = Node(data)
        new_node.left = self.NIL_LEAF
        new_node.right = self.NIL_LEAF
        
        parent = None
        curr = self.root
        while curr != self.NIL_LEAF:
            parent = curr
            if new_node.data < curr.data:
                curr = curr.left
            else:
                curr = curr.right
        
        new_node.parent = parent
        if parent is None:
            self.root = new_node 
        elif new_node.data < parent.data:
            parent.left = new_node
        else:
            parent.right = new_node
        
        new_node.color = "red"  # New node must be red
        self.insert_fixup(new_node)

    def insert_fixup(self, node):
        while node != self.root and node.parent.color == "red":
            if node.parent == node.parent.parent.left:  # Parent is a left child
                uncle = node.parent.parent.right
                if uncle.color == "red":  # Case 1: Uncle is red
                    node.parent.color = "black"
                    uncle.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent  # Move up the tree
                else:
                    if node == node.parent.right:  # Case 2: node is right child
                        node = node.parent
                        self.left_rotate(node)
                    # Case 3: node is a left child
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    self.right_rotate(node.parent.parent)
            else:  # Parent is a right child
                uncle = node.parent.parent.left
                if uncle.color == "red":  # Case 1: Uncle is red
                    node.parent.color = "black"
                    uncle.color = "black"
                    node.parent.parent.color = "red"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:  # Case 2: node is a left child
                        node = node.parent
                        self.right_rotate(node)
                    # Case 3: node is a right child
                    node.parent.color = "black"
                    node.parent.parent.color = "red"
                    self.left_rotate(node.parent.parent)
        
        self.root.color = "black"

    def delete(self, data):
        node_to_delete = self.search(data)
        if node_to_delete is None:
            print("Node with this value not found.")
            return
        self._delete_node_helper(node_to_delete)

    def _delete_node_helper(self, node):
        temp = node  # Используем временный узел
        original_color = temp.color  # Сохраняем цвет удаляемого узла

        if node.left == self.NIL_LEAF:
            substitute = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL_LEAF:
            substitute = node.left
            self._transplant(node, node.left)
        else:
            # Узел имеет двух детей, находим его преемника (минимальный узел в правом поддереве)
            temp = self.minimum(node.right)
            original_color = temp.color
            substitute = temp.right

            if temp.parent == node:
                substitute.parent = temp
            else:
                self._transplant(temp, temp.right)
                temp.right = node.right
                temp.right.parent = temp

            self._transplant(node, temp)
            temp.left = node.left
            temp.left.parent = temp
            temp.color = node.color

        if original_color == 'black':
            self._fix_delete(substitute)

    def _transplant(self, u, v):
        if u.parent == self.NIL_LEAF:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _fix_delete(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self._rotate_left(x.parent)
                    w = x.parent.right

                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        self._rotate_right(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.right.color = 'black'
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self._rotate_right(x.parent)
                    w = x.parent.left

                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self._rotate_left(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.left.color = 'black'
                    self._rotate_right(x.parent)
                    x = self.root

        x.color = 'black'

    def height(self, node):
        if node == self.NIL_LEAF:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL_LEAF:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL_LEAF:
            x.right.parent = y
        x.parent = y.parent

        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def search(self, data):
        return self._search(self.root, data)

    def _search(self, node, data):
        if node == self.NIL_LEAF or data == node.data:
            return node
        if data < node.data:
            return self._search(node.left, data)
        else:
            return self._search(node.right, data)

    def print_tree(self, node, level=0, prefix="Root:"):
        if node is not rbt.NIL_LEAF:
            print(" " * (level * 4) + prefix + " " + str(node.data) + " " + node.color)
            self.print_tree(node.left, level + 1, prefix="L---")
            self.print_tree(node.right, level + 1, prefix="R---")

    def bfs(self):
        if self.root is None:
            print("Tree is empty.")
            return

        queue = [self.root]
        while queue:
            node = queue.pop(0)
            if node.data!=None:
                print(node.data, end=" ")   
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    def display_in_ordered(self, node=None):
        if node is None:
            return 
        if node:
            self.display_in_ordered(node.left)
            if node.data!=None:
                print(node.data, end=" ")
            self.display_in_ordered(node.right)

    def display_pre_ordered(self, node=None):
        if node is None:
            return 
        if node:
            if node.data!=None:
                print(node.data, end=" ")
            self.display_pre_ordered(node.left)
            self.display_pre_ordered(node.right)

    def display_post_ordered(self, node=None):
        if node is None:
            return 
        if node:
            self.display_post_ordered(node.left)
            self.display_post_ordered(node.right)
            if node.data!=None:
                print(node.data, end=" ")


if __name__ == "__main__":
    rbt = RedBlackTree()

    elements = [10, 20, 30, 15, 25, 5, 1]
    for el in elements:
        rbt.insert(el)

    print(" Red-black tree after inserts:")
    rbt.print_tree(rbt.root)

    rbt.delete(5)
    print(" Red-black tree after removing 5:")
    rbt.print_tree(rbt.root)
    
    search_elements = [15, 99]
    for el in search_elements:
        result = rbt.search(el)
        if result != rbt.NIL_LEAF:
            print(f"\nElement {el} found.")
        else:
            print(f"\nElement {el} not found.")
    
    print("\nWide crawl:")
    rbt.bfs()

    print("\nDepth First Traversal Pre Ordered (Rlr):")
    rbt.display_pre_ordered(rbt.root)

    print("\nDepth First Traversal In Ordered (lRr):")
    rbt.display_in_ordered(rbt.root)

    print("\nDepth First Traversal Post Ordered (lrR):")
    rbt.display_post_ordered(rbt.root)

    print('\n')


# def experiment(num_insertions):
#     rb = RedBlackTree()
#     heights = []

#     for key in range(1, num_insertions + 1):
#         rb.insert(key)
#         heights.append(rb.height(rb.root))

#     return heights

# max_insertions = 1000
# heights = experiment(max_insertions)

# x_values = list(range(1, max_insertions + 1))

# plt.figure(figsize=(10, 6))
# plt.plot(x_values, heights, label='Tree height (measured)', color='blue')

# plt.plot(x_values, [ceil(2*np.log2(x+1)) for x in x_values], label='Theoretical maximum height 2*log(n+1)', color='orange', linestyle='--')
# plt.plot(x_values, [ceil(np.log2(x+1)) for x in x_values], label='Theoretical minimum height log(n+1)', color='red', linestyle='--')

# plt.title('Dependence of the height of the red-black tree on the number of keys')
# plt.xlabel('Number of keys n')
# plt.ylabel('Tree height h(n)')
# plt.legend()
# plt.grid()
# plt.show()
