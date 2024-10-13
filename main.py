from double_tree import double_tree as dbT
from double_tree_OPT import double_tree_OPT as dbT_OPT
import sys
import random
import math
import time


def record_height(tree, tree_OPT, file):

    prefectH = math.ceil(math.log2(tree.size))
    h1 = max(tree.T1.height, tree.T2.height)
    h2 = max(tree_OPT.T1.height, tree_OPT.T2.height)

    with open(file, 'wb') as f:
        f.write("tree " + (h1 - prefectH) + "tree_OPT" + (h2 - prefectH))


if __name__ == "__main__" :
    Size = int(sys.argv[1])
    file = 'size_'+ str(Size) + "_" + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())) + '.txt'

    for i in range(30):
        tree = dbT(Size)
        tree_OPT = dbT_OPT(Size)
        eraseNodes = [i for i in range(Size)]
        random.shuffle(eraseNodes)
        Max = [-1, -1, -1]
        count = Size / 4
        for i in eraseNodes :
            if count == 0 :break
            tree.erase_node(i)
            tree_OPT.erase_node(i)
            if tree.size == 0 : break 
            perfectH = math.ceil(math.log2(tree.size))
            h1 = max(tree.T1.height, tree.T2.height)
            h2 = max(tree_OPT.T1.height, tree_OPT.T2.height)
            if h2 - perfectH > 4 : 
                tree.print()
                tree_OPT.print()
            with open(file, 'a') as f:
                # f.write("tree = " + str(h1)  + "tree_OPT = " + str(h2) + "perfectH = " + str(perfectH) + "diff = " + str((h1 - h2)) + "\n")
                f.write('%d %d %d %d\n' %(h1, h2, perfectH, (h1 - h2)))
            Max[1] = max(Max[1], h1 - perfectH)
            Max[2] = max(Max[2], h2 - perfectH)
            Max[0] = max(Max[0], h1 - h2)
            count -= 1
        with open(file, 'a') as f:
            # f.write("max tree compare to perfect tree = " + str(Max[1]) + "max tree_OPT compare to perfect tree = " + str(Max[2]) + "max tree compare to tree_OPT" + str(Max[0]))
            f.write('   %d %d %d\n' %(Max[1], Max[2], Max[0]))





        
    
