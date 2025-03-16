class TreeNode:
    def __init__(self, rank, parent=None):
        self.rank = rank       # 节点唯一标识
        self.parent = parent   # 父节点引用
        self.children = []     # 子节点列表
    
    def __repr__(self):
        return f"Node({self.rank})"

class FTCO:
    def __init__(self, size=0, original_bandwidth=0):
        self.root = None
        self.nodes = {}                # {rank: TreeNode}
        self.original_bandwidth = original_bandwidth
        self._size = size               # 节点总数
        self._max_degree = 0           # 当前最大子节点数
        self.rewired_links = 0
        self.__initialize_by_size(size)

    @property
    def height(self):
        def dfs(node):
            if not node.children: 
                return 1
            return 1 + max(dfs(child) for child in node.children)
        return dfs(self.root) - 1 if self.root else 0

    @property
    def size(self):
        return self._size

    @property
    def bandwidth(self):
        """带宽 = 原始带宽 / 当前最大子节点数"""
        return self.original_bandwidth // max(1, self._max_degree)

    def __initialize_by_size(self, node_count):
       
        ranks = list(range(node_count))
        self._size = node_count
        self.root = TreeNode(ranks[0])
        self.nodes = {ranks[0]: self.root}
        
        # 层次遍历构建完全二叉树
        from collections import deque
        q = deque([self.root])
        idx = 1
        
        while q and idx < len(ranks):
            parent = q.popleft()
            
            # 添加左子节点
            if idx < len(ranks):
                left = TreeNode(ranks[idx], parent)
                parent.children.append(left)
                self.nodes[ranks[idx]] = left
                q.append(left)
                idx += 1
            
            # 添加右子节点
            if idx < len(ranks):
                right = TreeNode(ranks[idx], parent)
                parent.children.append(right)
                self.nodes[ranks[idx]] = right
                q.append(right)
                idx += 1
        
        self._max_degree = 2

    def erase_node(self, rank):
        """删除节点并重构拓扑"""
        if rank not in self.nodes:
            raise ValueError(f"节点 {rank} 不存在")
        
        target = self.nodes[rank]
        parent = target.parent
        
        # 删除根节点
        if not parent:
            if not target.children:
                self.root = None
            else:
                # 选择子节点中rank最小的作为新根
                new_root = min(target.children, key=lambda x: x.rank)
                new_root.parent = None
                
                # 将其他子节点转移到新根下
                for child in target.children:
                    if child != new_root:
                        new_root.children.append(child)
                        self.rewired_links += 1
                        child.parent = new_root
                self.root = new_root
        
        # 删除非根节点
        else:
            # 将目标节点的子节点转移给父节点
            for child in target.children:
                child.parent = parent
                parent.children.append(child)
                self.rewired_links += 1
            parent.children.remove(target)
        
        del self.nodes[rank]
        self._size -= 1
        
        # 重新计算最大子节点数
        self._max_degree = max(len(node.children) for node in self.nodes.values()) if self.nodes else 0

    def print_tree(self):
        """可视化树结构"""
        def print_helper(node, level=0):
            if not node: return
            print("  " * level + str(node))
            for child in sorted(node.children, key=lambda x: x.rank):
                print_helper(child, level + 1)
        
        print(f"Tree (height={self.height}, size={self.size}, bandwidth={self.bandwidth})")
        print_helper(self.root)

