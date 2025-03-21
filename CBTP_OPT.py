from binarytree import Node, get_parent, get_index
import math 

class Tree :
    root = None             # 根节点
    specialNode = None    # 特殊节点
    singleNode = None     # 单树节点

    @property
    def height(self):
        if self.root == None: return 0
        return self.root.height

    def print(self):
        print(self.root)

class CBTP_OPT :
    
    T1 = Tree()
    T2 = Tree()
    size = 0                #节点总数

    def __init__(self, size):
        self.size = size
        self.T1.root = self.__T1()
        self.T2.root = self.__T2()
        self.height = max(self.T1.height, self.T2.height)
        self.rewired_links = 0
        self.__find_singleNode(self.T1)
        self.__find_singleNode(self.T2)
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
        return self.__create_T1(self.size, 0)

    def __T2(self):
        if(self.size % 2 != 0):
            return self.__shift_tree(self.T1.root)
        else: 
            return self.__mirror_tree(self.T1.root)
    
    def __singleNode(self, node, result=None) :
        if result is None:
            result = []
        if node is None:
            return result
        # 检查当前节点是否只有一个子树
        if (node.left is None and node.right is not None) or (node.left is not None and node.right is None):
            result.append(node)
        # 递归遍历左子树和右子树
        self.__singleNode(node.left, result)
        self.__singleNode(node.right, result)
        return result

    def __find_singleNode(self, T):
        T.singleNode = self.__singleNode(T.root)

    def __find_specialNode(self):
        # 节点数量为偶数时不存在特殊节点
        if self.size % 2 == 0 :
            self.T1.specialNode = None
            self.T2.specialNode = None
            return 
        # 求两棵树叶子节点集合的交集
        values1 = {node.value for node in self.T1.root.leaves}
        values2 = {node.value for node in self.T2.root.leaves}
        intersection_value = values1.intersection(values2)
        # 因为只会有一个特殊节点，所以可以直接取出第一个值
        special_value = next(iter(intersection_value))
        for node in self.T1.root.leaves :
            if node.value == special_value :
                self.T1.specialNode = node
                break
        for node in self.T2.root.leaves :
            if node.value == special_value :
                self.T2.specialNode = node
                break

    def __is_leaf(self, T, value) :
        for node in T.root.leaves :
            if node.value == value :
                return True
        return False

    def __find_node(self, root, value):
        if root is None:
            return None
        if root.value == value:
            return root
        left_result = self.__find_node(root.left, value)
        if left_result is not None:
            return left_result
        return self.__find_node(root.right, value)

    def __level(self, root, node, level = 1):
        if root is None:
            return -1  # 节点未找到
        if root.value == node.value:
            return level
        # 在左子树中查找
        left_level = self.__level(root.left, node, level + 1)
        if left_level != -1:
            return left_level
        # 在右子树中查找
        return self.__level(root.right, node, level + 1)

    def __insert(self, pre, insNode):
        if pre.left == None:
            pre.left = insNode
        else : 
            pre.right = insNode
        insNode.parent = pre
        self.rewired_links += 1

    def __del(self, pre, node):
        if pre.left != None and pre.left.value == node.value :
            pre.left = None
        elif pre.right != None and pre.right.value == node.value :
            pre.right = None
        node.parent = None
            
    def __merge_singleNode(self, T):
        self.__find_singleNode(T)
        if len(T.singleNode) < 2 : return

        # 优化点
        # 当两个节点level相同时，这时它们是兄弟节点，此时的更优解的合并方法是将子树高的那个节点取出来连接到它的兄弟节点，它的子树就连接到pre上，这样可以使树高降低
        if self.__level(T.root, T.singleNode[0]) == self.__level(T.root, T.singleNode[1]):
            if T.singleNode[0].height >= T.singleNode[1].height :
                insNode,recvNode = T.singleNode[0], T.singleNode[1]  
            else:
                insNode,recvNode = T.singleNode[1], T.singleNode[0]
            pre = get_parent(T.root, insNode)
            child = insNode.left if insNode.left != None else insNode.right
            self.__del(pre, insNode)
            self.__del(insNode, child)
            self.__insert(pre, child)
            self.__insert(recvNode, insNode)
            return
        
        insNode = T.singleNode[0] if self.__level(T.root, T.singleNode[0]) >= self.__level(T.root, T.singleNode[1]) else T.singleNode[1]
        recvNode = T.singleNode[0] if insNode.value == T.singleNode[1].value else T.singleNode[1]

        if insNode.left != None :
            inschild = insNode.left
            insNode.left = None
        else :
            inschild = insNode.right
            insNode.right = None            
        self.__insert(recvNode, inschild)

    def erase_node(self, value):
        if self.__find_node(self.T1.root, value) == None :
            return -1
        if self.size == 1 :
            self.T1.root = None
            self.T2.root = None
            self.T1.specialNode = None
            self.T2.specialNode = None
            return 0
        # 删除节点都是叶节点即是特殊节点
        if self.__is_leaf(self.T1, value) and self.__is_leaf(self.T2, value):
            # 找到特殊节点后删去
            pre1 = get_parent(self.T1.root, self.T1.specialNode)
            pre2 = get_parent(self.T2.root, self.T2.specialNode)
            self.__del(pre1, self.T1.specialNode)
            self.__del(pre2, self.T2.specialNode)
            self.T1.specialNode = None
            self.T2.specialNode = None

        # 删除节点在一棵树中是叶子节点，另一棵树里不是
        else :
            leaf_tree = self.T1 if self.__is_leaf(self.T1, value) else self.T2
            noleaf_tree = self.T2 if self.__is_leaf(self.T1, value) else self.T1
            # 先处理叶子节点的树
            node = self.__find_node(leaf_tree.root, value)
            pre = get_parent(leaf_tree.root, node)
            self.__del(pre, node)
            self.__merge_singleNode(leaf_tree)
            # 然后处理非叶节点的树
            node = self.__find_node(noleaf_tree.root, value)
            # 存在特殊节点则直接替换
            if noleaf_tree.specialNode != None :
                node.value = noleaf_tree.specialNode.value
                self.rewired_links += 3
                
                del noleaf_tree.root[get_index(noleaf_tree.root, noleaf_tree.specialNode)]
            # 不存在特殊节点就一定存在单树节点
            else :
                # 删除节点为单树节点时，直接将子节点连接到父节点上
                if node.value == noleaf_tree.singleNode[0].value :
                    child = node.left if node.left != None else node.right
                    pre = get_parent(noleaf_tree.root, node)
                    if pre != None :
                        self.__del(pre, node)
                        self.__insert(pre, child)
                    else :
                        noleaf_tree.root = child
                
                else :
                    # 优化点
                    # 直接用单树节点进行替换
                    pre = get_parent(noleaf_tree.root, noleaf_tree.singleNode[0])
                    # 删除节点是根节点
                    if noleaf_tree.singleNode[0].left == None :
                        insert_node = noleaf_tree.singleNode[0].right
                    else : insert_node = noleaf_tree.singleNode[0].left

                    self.__del(noleaf_tree.singleNode[0], insert_node)
                    if pre != None:
                        self.__del(pre, noleaf_tree.singleNode[0])
                        self.__insert(pre, insert_node)
                    else:
                        noleaf_tree.root = insert_node

                    node.value = noleaf_tree.singleNode[0].value
                    self.rewired_links += 3
                    

                    

        self.size -= 1                
        self.__find_specialNode()
        self.__find_singleNode(self.T1)
        self.__find_singleNode(self.T2)
        self.height = max(self.T1.height, self.T2.height)

    def __calculate_depth(self, node, target, depth=0):
        if node is None:
            return -1 
        if node == target:
            return depth
        left_depth = self.__calculate_depth(node.left, target, depth + 1)
        if left_depth != -1:
            return left_depth
        right_depth = self.__calculate_depth(node.right, target, depth + 1)
        return right_depth

    def add_node(self, value):
        addNode1 = Node(value)
        addNode2 = Node(value)
        if len(self.T1.singleNode) != 0 :
            self.__insert(self.T1.singleNode[0], addNode1)
            self.__insert(self.T2.singleNode[0], addNode2)
        else :
            #优化点：插入时调整特殊节点的位置
            if self.__calculate_depth(self.T1.root, self.T1.specialNode) != self.T1.root.min_leaf_depth :
                for leaf in self.T1.root.levelorder :
                    if leaf.height == 0 :
                        min_depth_leave1 = leaf
                        break  
                self.T1.specialNode.value, min_depth_leave1.value = min_depth_leave1.value, self.T1.specialNode.value
                self.rewired_links += 2

            if self.__calculate_depth(self.T2.root, self.T2.specialNode) != self.T2.root.min_leaf_depth :
                for leaf in self.T2.root.levelorder :
                    if leaf.height == 0 :
                        min_depth_leave2 = leaf
                        break  
                self.T2.specialNode.value, min_depth_leave2.value = min_depth_leave2.value, self.T2.specialNode.value
                self.rewired_links += 1
            self.__find_specialNode()
            
            self.__insert(self.T1.specialNode, addNode1)
            pre = get_parent(self.T2.root, self.T2.specialNode)
            self.__del(pre, self.T2.specialNode) 
            self.__insert(pre, addNode2)
            self.__insert(addNode2, self.T2.specialNode)
        
        self.size += 1                
        self.__find_specialNode()
        self.__find_singleNode(self.T1)
        self.__find_singleNode(self.T2)
        self.height = max(self.T1.height, self.T2.height)

    def print(self):
        self.T1.print()
        self.T2.print()