import random

#Node class
class Node(object): 
    def __init__(self, value): 
        self.value = value 
        self.left = None
        self.right = None
        self.height = 1


#Create a BST as base/for comparison to AVL
class BST():
    def getHeight(self, root): 
        if root == None:
            return 0
        else:
            return root.height

    def getMaxHeight(self, root):
        return max(self.getHeight(root.left), self.getHeight(root.right))

    def getEdges(self,root):
        edge_list = []
        if root == None:
            return edge_list
        
        if type(root.left) != 'NoneType':
            left_edge = (root, root.left)
            edge_list.append(left_edge)
        if type(root.right) != 'NoneType':
            right_edge = (root, root.right)
            edge_list.append(right_edge)
        
        edge_list += self.getEdges(root.left)
        edge_list += self.getEdges(root.right)
        
        return edge_list


    def getPreorderTraversal(self, root): 
        node_list = []

        if root:
            node_list.append(root.value)
            node_list += self.getPreorderTraversal(root.left)
            node_list += self.getPreorderTraversal(root.right) 

        else:
            return node_list

        return node_list


    def insertValue(self, root, insert_value): 
        if root == None: 
            return Node(insert_value) 
        elif insert_value < root.value: 
            root.left = self.insertValue(root.left, insert_value) 
        else: 
            root.right = self.insertValue(root.right, insert_value) 

        root.height = 1 + self.getMaxHeight(root)
        return root 
  



#AVL Tree class        
class AVL(BST):
    #Initiate Binary Search Tree Class
    def __init__(self):
        super().__init__()

    #define rotate functions
    #rotate functions
    def rotateRight(self, n): 
        previous_left = n.left
        new_left = previous_left.right
        previous_left.right = n
        n.left = new_left
  
        n.height = 1 + self.getMaxHeight(n)
        previous_left.height = 1 + self.getMaxHeight(previous_left)

        return previous_left

    def rotateLeft(self, n):   
        previous_right = n.right
        new_right = previous_right.left
        previous_right.left = n
        n.right = new_right

        n.height = 1 + self.getMaxHeight(n)
        previous_right.height = 1 + self.getMaxHeight(previous_right)

        return previous_right

    #update insertValue to implemnt AVL algorithm
    def insertValue(self, root, insert_value):
        #insert value as if normal BST
        root = super().insertValue(root, insert_value)

        #AVL algorithm 
        #check to see if the tree needs rebalancing
        #left height is more than 1 additional branch higher than right.  rotate offending subtree right
        if (self.getHeight(root.left) - self.getHeight(root.right)) > 1:
            #if true left-right, else right
            if insert_value > root.left.value:
                root.left = self.rotateLeft(root.left)
            return self.rotateRight(root)

        #if balance is less than -1 - if right height is more than 1 additional branch higher than left height.  rotate offending subtree left
        if (self.getHeight(root.left) - self.getHeight(root.right) )< -1:
            #if true, right-left, else left
            if insert_value < root.right.value:
                root.right = self.rotateRight(root.right)
            return self.rotateLeft(root)

        return root 
  

          


import time
from random import randint
import numpy as np


def buildInitialAVLTree(initial_values):
    tree = AVL()
    root = None

    for v in initial_values:
        root = tree.insertValue(root, v)
    return tree, root

def buildInitialBSTTree(initial_values):
    tree = BST()
    root = None

    for v in initial_values:
        root = tree.insertValue(root, v)
    return tree, root


def treeSearch(search_value, tree, root, count = 0):
    if search_value == root.value:
        count +=1
    elif search_value > root.value:
        count+=1
        try:
            count = treeSearch(search_value, tree, root.right, count)
        except:
            pass
    elif search_value < root.value:
        count+=1
        try:
            count = treeSearch(search_value, tree, root.left, count)
        except:
            pass
    return count
    



#Tests - random array
print("Random Array Test\n\n")
import time
from random import randint
import numpy as np

tests_per_size = 10
current_size = 8
max_size = 131072

def BST_test(test_array):
    start = time.time()
    BST_Tree, BST_TreeRoot = buildInitialBSTTree(test_array)
    end = time.time()
    return BST_Tree, BST_TreeRoot, (end - start)

def AVL_test(test_array):
    start = time.time()
    AVL_Tree, AVL_TreeRoot = buildInitialAVLTree(test_array)
    end = time.time()
    return AVL_Tree, AVL_TreeRoot, (end - start)

def treeTest(current_size, tests_per_size):
    BST_time = 0
    AVL_time = 0
    BST_search_count = []
    AVL_search_count = []
    BST_height = []
    AVL_height = []
    for i in range(tests_per_size):
        test_array = [randint(0,1000000) for i in range(current_size)]
        BST_Tree, BST_TreeRoot, BST_build_time = BST_test(test_array)
        BST_height.append(BST_Tree.getHeight(BST_TreeRoot))
        AVL_Tree, AVL_TreeRoot, AVL_build_time = AVL_test(test_array)
        AVL_height.append(AVL_Tree.getHeight(AVL_TreeRoot))
        BST_time += BST_build_time
        AVL_time += AVL_build_time
        for j in test_array:
            BST_search_count.append(treeSearch(j, BST_Tree, BST_TreeRoot))
            AVL_search_count.append(treeSearch(j, AVL_Tree, AVL_TreeRoot))

    return BST_time / tests_per_size, AVL_time / tests_per_size, BST_search_count, AVL_search_count, BST_height, AVL_height, 


while current_size <= max_size:
    avg_BST_build_time, avg_AVL_build_time, BST_search_count, AVL_search_count, BST_height, AVL_height = treeTest(current_size, tests_per_size)
    
    print(f'Average time to construct a BST of {current_size}:  {avg_BST_build_time: 0.5f}')
    print(f'Average number of comparisons to find value in BST Tree: {np.mean(BST_search_count): 0.3f}')
    BST_search_count.sort()
    print(f'worst case scenario for number of comparisons to find value in BST Tree: {BST_search_count[-1]}')
    print(f'Average height for a BST: {np.mean(BST_height): 0.1f}\n')
    print(f'Average time to construct a AVL of {current_size}:  {avg_AVL_build_time: 0.5f}')
    print(f'Average number of comparisons to find value in AVL Tree: {np.mean(AVL_search_count): 0.3f}')
    AVL_search_count.sort()
    print(f'worst case scenario for number of comparisons to find value in AVL Tree: {AVL_search_count[-1]}')
    print(f'Average height for a BST: {np.mean(AVL_height): 0.1f}\n\n')
    current_size *= 2


#test using sorted list
print("Sorted Array Test\n\n")
tests_per_size = 10
current_size = 8
max_size = 2048

def BST_test_sorted(test_array):
    start = time.time()
    BST_Tree, BST_TreeRoot = buildInitialBSTTree(test_array)
    end = time.time()
    return BST_Tree, BST_TreeRoot, (end - start)

def AVL_test_sorted(test_array):
    start = time.time()
    AVL_Tree, AVL_TreeRoot = buildInitialAVLTree(test_array)
    end = time.time()
    return AVL_Tree, AVL_TreeRoot, (end - start)

def treeTestSorted(current_size, tests_per_size):
    BST_time = 0
    AVL_time = 0
    BST_search_count = []
    AVL_search_count = []
    BST_height = []
    AVL_height = []
    for i in range(tests_per_size):
        test_array = sorted([randint(0,1000000) for i in range(current_size)], key = lambda x: x, reverse = False)
        BST_Tree, BST_TreeRoot, BST_build_time = BST_test_sorted(test_array)
        BST_height.append(BST_Tree.getHeight(BST_TreeRoot))
        AVL_Tree, AVL_TreeRoot, AVL_build_time = AVL_test_sorted(test_array)
        AVL_height.append(AVL_Tree.getHeight(AVL_TreeRoot))
        BST_time += BST_build_time
        AVL_time += AVL_build_time
        for j in test_array:
            BST_search_count.append(treeSearch(j, BST_Tree, BST_TreeRoot))
            AVL_search_count.append(treeSearch(j, AVL_Tree, AVL_TreeRoot))

    return BST_time / tests_per_size, AVL_time / tests_per_size, BST_search_count, AVL_search_count, BST_height, AVL_height, 


while current_size <= max_size:
    avg_BST_build_time, avg_AVL_build_time, BST_search_count, AVL_search_count, BST_height, AVL_height = treeTestSorted(current_size, tests_per_size)
    
    print(f'Average time to construct a BST of {current_size}:  {avg_BST_build_time: 0.5f}')
    print(f'Average number of comparisons to find value in BST Tree: {np.mean(BST_search_count): 0.3f}')
    BST_search_count.sort()
    print(f'worst case scenario for number of comparisons to find value in BST Tree: {BST_search_count[-1]}')
    print(f'Average height for a BST: {np.mean(BST_height): 0.1f}\n')
    print(f'Average time to construct a AVL of {current_size}:  {avg_AVL_build_time: 0.5f}')
    print(f'Average number of comparisons to find value in AVL Tree: {np.mean(AVL_search_count): 0.3f}')
    AVL_search_count.sort()
    print(f'worst case scenario for number of comparisons to find value in AVL Tree: {AVL_search_count[-1]}')
    print(f'Average height for a BST: {np.mean(AVL_height): 0.1f}\n\n')
    current_size *= 2
