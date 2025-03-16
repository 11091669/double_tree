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

class CBTP :
    
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
        insNode, recvNode = sorted(T.singleNode, key=lambda x: self.__level(T.root, x), reverse=True)[:2]
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
            # 存在特殊节点则插入特殊节点
            if noleaf_tree.specialNode != None :
                pre = get_parent(noleaf_tree.root, node)
                if pre != None:
                    self.__del(pre, node)
                    if self.__find_node(node.left, noleaf_tree.specialNode.value) != None:
                        self.__insert(pre, node.left)
                        self.__insert(noleaf_tree.specialNode, node.right)
                    else :
                        self.__insert(pre, node.right)
                        self.__insert(noleaf_tree.specialNode, node.left)
                else :
                    if self.__find_node(node.left, noleaf_tree.specialNode.value) != None:
                        noleaf_tree.root = node.left
                        self.__insert(noleaf_tree.specialNode, node.right)
                    else :
                        noleaf_tree.root = node.right
                        self.__insert(noleaf_tree.specialNode, node.left)
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
                    # 删除节点的子树不包含单树节点，默认将左子树接在pre，右子树接在单树节点
                    if len(self.__singleNode(node.left)) == 0 and len(self.__singleNode(node.right)) == 0 :
                        pre = get_parent(noleaf_tree.root, node)
                        if pre != None:
                            self.__del(pre, node)
                            self.__insert(pre, node.left)
                            self.__insert(noleaf_tree.singleNode[0], node.right)
                        else :
                            noleaf_tree.root = node.left
                            self.__insert(noleaf_tree.singleNode[0], node.right)

                    # 否则将包含单树节点的子树接在pre，不包含的子树接在单树节点
                    else :
                        withSingleNode = node.left if len(self.__singleNode(node.left)) != 0 else node.right
                        noSingleNode = node.left if len(self.__singleNode(node.left)) == 0 else node.right
                        pre = get_parent(noleaf_tree.root, node)
                        if pre != None :
                            self.__del(pre, node)
                            self.__insert(pre, withSingleNode)
                            self.__insert(noleaf_tree.singleNode[0], noSingleNode)
                        else :
                            noleaf_tree.root = withSingleNode
                            self.__insert(noleaf_tree.singleNode[0], noSingleNode)

        self.size -= 1                
        self.__find_specialNode()
        self.__find_singleNode(self.T1)
        self.__find_singleNode(self.T2)
        self.height = max(self.T1.height, self.T2.height)

    def add_node(self, value):
        addNode1 = Node(value)
        addNode2 = Node(value)
        if len(self.T1.singleNode) != 0 :
            self.__insert(self.T1.singleNode[0], addNode1)
            self.__insert(self.T2.singleNode[0], addNode2)
        else :
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

if __name__ == "__main__" :
    # 测试删除序列 [498, 451, 135, ...] 的前10个节点
    test_nodes = [354, 394, 459, 204, 497, 423, 227, 316, 243, 159, 56, 165, 301, 176, 38, 336, 140, 137, 276, 490, 400, 272, 315, 352, 114, 270, 233, 447, 462, 99, 70, 143, 197, 476, 224, 330, 364, 307, 39, 369, 167, 404, 115, 4, 179, 302, 15, 18, 193, 110, 318, 390, 246, 392, 367, 347, 189, 61, 471, 235, 343, 77, 119, 439, 180, 464, 288, 321, 157, 63, 262, 129, 10, 457, 428, 73, 446, 22, 381, 271, 329, 443, 200, 361, 429, 106, 122, 311, 312, 162, 387, 463, 357, 141, 9, 46, 411, 207, 435, 23, 360, 340, 417, 40, 492, 11, 215, 239, 44, 280, 313, 120, 265, 419, 19, 406, 134, 210, 158, 229, 188, 249, 97, 268, 76, 154, 103, 427, 437, 118, 258, 55, 232, 355, 474, 186, 396, 412, 82, 74, 264, 92, 164, 85, 109, 43, 12, 478, 252, 484, 202, 363, 205, 170, 183, 332, 291, 65, 69, 84, 136, 116, 274, 458, 498, 131, 309, 37, 48, 275, 267, 88, 95, 465, 50, 231, 287, 26, 240, 454, 445, 399, 338, 27, 414, 161, 323, 402, 297, 353, 24, 282, 166, 96, 452, 362, 13, 25, 253, 16, 20, 51, 418, 482, 494, 424, 219, 29, 289, 299, 420, 261, 112, 256, 370, 123, 36, 152, 223, 66, 477, 196, 221, 292, 365, 480, 300, 451, 14, 310, 42, 98, 125, 281, 410, 378, 483, 251, 47, 344, 226, 296, 171, 331, 146, 317, 100, 273, 175, 397, 139, 304, 426, 185, 432, 374, 327, 393, 135, 466, 172, 111, 60, 335, 217, 486, 433, 325, 187, 30, 481, 376, 208, 244, 391, 334, 468, 194, 345, 155, 17, 101, 71, 395, 212, 150, 238, 105, 250, 409, 407, 173, 373, 358, 416, 339, 242, 359, 487, 33, 57, 285, 68, 237, 283, 75, 488, 349, 372, 469, 319, 160, 266, 199, 21, 79, 149, 163, 448, 431, 107, 430, 375, 255, 440, 279, 182, 64, 7, 442, 203, 377, 59, 49, 263, 461, 222, 450, 2, 32, 366, 259, 467, 385, 121, 415, 230, 58, 178, 341, 384, 346, 108, 388, 473, 78, 389, 470, 491, 305, 34, 485, 147, 441, 216, 444, 383, 456, 130, 453, 102, 320, 177, 206, 191, 89, 322, 460, 91, 386, 496, 303, 449, 113, 225, 260, 87, 0, 86, 168, 220, 236, 368, 5, 499, 67, 234, 94, 6, 201, 8, 126, 3, 181, 475, 117, 413, 324, 403, 350, 127, 151, 379, 351, 133, 495, 218, 90, 277, 28, 148, 421, 337, 401, 144, 81, 293, 308, 245, 62, 405, 284, 247, 408, 211, 248, 83, 398, 142, 356, 434, 45, 153, 333, 241, 479, 278, 52, 72, 192, 104, 328, 436, 314, 295, 290, 54, 294, 380, 53, 31, 425, 128, 342, 35, 326, 156, 80, 1, 145, 257, 422, 184, 489, 174, 228, 254, 269, 472, 132, 455, 93, 371, 209, 298, 195, 438, 190, 214, 138, 198, 286, 348, 124, 213, 493, 169, 41, 306, 382]
    cbtp = CBTP(size=500)
    for node in test_nodes:
        cbtp.erase_node(node)
        cbtp.print()  # 输出当前树结构