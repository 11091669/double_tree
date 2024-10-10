from binarytree import Node, get_parent
import math 

class double_tree :
    
    __specialNodeT1 = None  # T1的特殊节点
    __specialNodeT2 = None  # T2的特殊节点
    __singleNodeT1 = None   # T1的单树节点
    __singleNodeT2 = None   # T2的单树节点
    T1 = None
    T2 = None
    size = 0                #节点总数

    def __init__(self, size):
        self.size = size
        self.__T1()
        self.__T2()  
        self.__find_specialNode()

    # 构建完全二叉树
    def __create_complete_binary_tree(self, start, end):
        if start > end:
            return None
        mid = (start + end) // 2
        root = Node(mid)
        root.left = self.__create_complete_binary_tree(start, mid - 1)
        root.right = self.__create_complete_binary_tree(mid + 1, end)
        return root
    
    #递归构造T1
    def __create_T1(self, size, start): 
        if size <= 0:
            return None
        # 根据公式计算h
        h = math.ceil(math.log2(size + 1))
        # 计算中心节点的rank值
        rootRank = 2**(h - 1) - 1 + start
        root = Node(rootRank)
        left_subtree_size = rootRank - start
        right_subtree_size = size - 1 - left_subtree_size
        # 左子树为一棵完全二叉树
        root.left = self.__create_complete_binary_tree(start, left_subtree_size - 1 + start)
        # 右子树进行递归构造
        root.right = self.__create_T1(right_subtree_size, rootRank + 1)
        return root

    def __mirror_tree(self, node):
        if node is None:
            return None
        new_value = self.size - node.value - 1
        new_node = Node(new_value)
        new_node.left = self.__mirror_tree(node.left)
        new_node.right = self.__mirror_tree(node.right)
        return new_node

    def __shift_tree(self, node):
        if node is None:
            return None
        new_value = (node.value + 1) % self.size
        new_node = Node(new_value)
        new_node.left = self.__shift_tree(node.left)
        new_node.right = self.__shift_tree(node.right)
        return new_node

    def __T1(self):
        if self.size <= 0:
            return None
        self.T1 = self.__create_T1(self.size, 0)

    def __T2(self):
        if(self.size % 2 != 0):
            self.T2 = self.__shift_tree(self.T1)
        else: 
            self.T2 = self.__mirror_tree(self.T1)
    
    def __find_singleNode(self,node):
        if result is None:
            result = []
        if node is None:
            return result
        # 检查当前节点是否只有一个子树
        if (node.left is None and node.right is not None) or (node.left is not None and node.right is None):
            result.append(node)
        # 递归遍历左子树和右子树
        self.__find_singleNode(node.left, result)
        self.__find_singleNode(node.right, result)
        return result

    def __find_specialNode(self):
        # 求两棵树叶子节点集合的交集
        values1 = {node.value for node in self.T1.leaves}
        values2 = {node.value for node in self.T2.leaves}
        intersection_value = values1.intersection(values2)
        # 因为只会有一个特殊节点，所以可以直接取出第一个值
        special_value = next(iter(intersection_value))
        for node in self.T1.leaves :
            if node.value == special_value :
                self.__specialNodeT1 = node
                break
        for node in self.T2.leaves :
            if node.value == special_value :
                self.__specialNodeT2 = node
                break
        
    
    def print(self):
        print(self.T1)
        print(self.T2)

tree = double_tree(11)
tree.print() 

