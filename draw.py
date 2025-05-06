import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
import csv
import pandas as pd
from core import Network
from matplotlib.font_manager import FontProperties
import matplotlib.font_manager as fm
import sys

# 全局样式设置
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
BAR_WIDTH = 0.2
FIGURE_SIZE = (5, 3.75)
FIGURE_SIZE2 = (4, 3)
COLOR_DICT = {
    'CBTP': '#f9e7a7',
    'CBTP_OPT': '#b2df8a',
    'FTCO': '#ef767b',
    'binary_tree': '#43a3ef'
}
COLOR_DICT_LINE = {
    'CBTP': '#dda43d',
    'CBTP_OPT': 'green',
    'FTCO': 'red',
    'binary_tree': 'blue'
}


LINE_STYLES = {
    'CBTP': ['-'],
    'CBTP_OPT': ['--'],
    'FTCO': [':'],
    'binary_tree': ['-.']
}

font_size = 17

font_size2 = 12


# 定义边框颜色和线宽
edge_color = 'black'
line_width = 1

ReadDir = f'/home/sx/double_tree/double_tree/result_bandwith{Network.bandwidth}_rewiredtime{Network.rewired_time}_timestep{Network.time_step}_latency{Network.latency}/'
SaveDir = f'./pictures_bandwith{Network.bandwidth}_rewiredtime{Network.rewired_time}_timestep{Network.time_step}_latency{Network.latency}/'

# 创建目录（如果目录不存在）
if not os.path.exists(SaveDir):
    os.makedirs(SaveDir)
    print(f"目录已创建: {SaveDir}")
else:
    print(f"目录已存在: {SaveDir}")


# 柱形图
# 横坐标：节点数
# 纵坐标：树高
# 方案：FTCO、CBTP、CBTP_OPT、新建二叉树
def height_nof():
    data = pd.read_csv(ReadDir + 'height_nof.csv')
    fig, ax = plt.subplots(figsize=FIGURE_SIZE2)

    x_labels = data['Node_num']  # 横坐标的标签
    x = range(len(x_labels))
    CBTP = data['CBTP']
    CBTP_OPT = data['CBTP_OPT']
    FTCO = data['FTCO']
    binary_tree = data['binary_tree']



    # 绘制四组柱状图（每组偏移一个柱宽）
    rects1 = ax.bar([i - 1.5 * BAR_WIDTH for i in x], CBTP,
                    width=BAR_WIDTH * 0.7, color=COLOR_DICT['CBTP'], label='CBTP'
                    ,edgecolor = edge_color, linewidth=line_width)
    rects2 = ax.bar([i - 0.5 * BAR_WIDTH for i in x], CBTP_OPT,
                    width=BAR_WIDTH* 0.7, color=COLOR_DICT['CBTP_OPT'], label='CBTP-HO'
                    ,edgecolor = edge_color, linewidth=line_width)
    rects3 = ax.bar([i + 0.5 * BAR_WIDTH for i in x], FTCO,
                    width=BAR_WIDTH* 0.7, color=COLOR_DICT['FTCO'], label='FTCO'
                    ,edgecolor = edge_color, linewidth=line_width)
    rects4 = ax.bar([i + 1.5 * BAR_WIDTH for i in x], binary_tree,
                    width=BAR_WIDTH* 0.7, color=COLOR_DICT['binary_tree'], label='Binary Tree'
                    ,edgecolor = edge_color, linewidth=line_width)

    ax.set_xlabel("Number of Nodes", fontsize=font_size2)
    ax.set_ylabel("Height of Tree", fontsize=font_size2)
    ax.set_ylim(5, 11)

    ax.set_title("", fontsize=11)
    # 设置 x 轴的刻度标签
    plt.xticks(x, x_labels)

    ax.legend(loc='upper left')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    if not os.path.exists(SaveDir):
        os.makedirs(SaveDir)
    SaveFile = SaveDir + "height_nof" + '.pdf'
    fig.savefig(SaveFile)
    print(SaveFile + ' ==================>>> has been complete')
    plt.close()


# 折线图
# 横坐标：故障数
# 纵坐标：树高
# 方案：FTCO、CBTP、CBTP_OPT、新建二叉树
# 不同节点数对应不同图
def height_withf():
    Sizes = [128, 256, 512, 1024]
    for size in Sizes:
        data_list = []
        for n in range(1, 11):
            data_list.append(pd.read_csv(ReadDir + f'height_withf_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        fig, ax = plt.subplots(figsize=FIGURE_SIZE2)

        x = range(size)
        CBTP = data['CBTP']
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']
        binary_tree = data['binary_tree']

        ax.plot(x, CBTP, label='CBTP', linestyle=LINE_STYLES['CBTP'][0], color=COLOR_DICT_LINE['CBTP'])
        ax.plot(x, CBTP_OPT, label='CBTP-HO', linestyle=LINE_STYLES['CBTP_OPT'][0], color=COLOR_DICT_LINE['CBTP_OPT'])
        ax.plot(x, FTCO, label='FTCO', linestyle=LINE_STYLES['FTCO'][0], color=COLOR_DICT_LINE['FTCO'])
        ax.plot(x, binary_tree, label='binary_tree', linestyle=LINE_STYLES['binary_tree'][0], color=COLOR_DICT_LINE['binary_tree'])

        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.set_xlabel("Number of Leave Nodes", fontsize=font_size)
        ax.set_ylabel("Height of Tree", fontsize=font_size)
        ax.set_ylim(0, max(CBTP) + 2)
        ax.set_xlim(0, size)
        title = f'Cluster Size = {size}'
        ax.set_title(title, fontsize=font_size)
        ax.legend(loc='upper right')
        ax.set_axisbelow(True)
        ax.grid(True,which='both')
        plt.tight_layout()

        if not os.path.exists(SaveDir):
            os.makedirs(SaveDir)
        SaveFile = SaveDir + f"height_withf_size{size}" + '.pdf'
        fig.savefig(SaveFile)
        print(SaveFile + ' ==================>>> has been complete')
        plt.close()


# 柱形图
# 横坐标：数据大小
# 纵坐标：Allreduce完成时间
# 方案：FTCO、CBTP_OPT
# 不同节点数对应不同图
def Allreduce_nof():
    Sizes = [128, 256, 512, 1024]
    for size in Sizes:
        data = pd.read_csv(ReadDir + f'Allreduce_nof_size{size}.csv')

        fig, ax = plt.subplots(figsize=FIGURE_SIZE2)

        x_labels = ['10KB','10MB',"1GB",'10GB','100GB'] # 横坐标的标签
        x = range(len(x_labels))
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']

        rects2 = ax.bar([i - 0.5 * BAR_WIDTH for i in x], CBTP_OPT,
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['CBTP_OPT'], label='CBTP-HO'
                        ,edgecolor = edge_color, linewidth=line_width)
        rects3 = ax.bar([i + 0.5 * BAR_WIDTH for i in x], FTCO,
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['FTCO'], label='FTCO'
                        ,edgecolor = edge_color, linewidth=line_width)

        ax.set_xlabel("Datasize", fontsize=font_size2)
        ax.set_ylabel("AllReduce \nCompletion Time (s)", fontsize=font_size2)

        # 设置纵坐标为对数刻度
        ax.set_yscale('log')

        title = f'Cluster Size = {size}'
        ax.set_title(title, fontsize=font_size2)
        # 设置 x 轴的刻度标签
        plt.xticks(x, x_labels)
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        ax.legend()

        plt.tight_layout()

        if not os.path.exists(SaveDir):
            os.makedirs(SaveDir)
        SaveFile = SaveDir + f"Allreduce_nof_size{size}" + '.pdf'
        fig.savefig(SaveFile)
        print(SaveFile + ' ==================>>> has been complete')
        plt.close()    


# 柱形图
# 横坐标：节点数
# 纵坐标：Allreduce完成时间
# 方案：FTCO、CBTP_OPT
# 不同数据大小对应不同图
def Allreduce_nof2():
    Sizes = [128, 256, 512, 1024]
    all_data = []

    # 读取所有尺寸的数据
    for size in Sizes:
        data = pd.read_csv(ReadDir + f'Allreduce_nof_size{size}.csv')
        data['size'] = size  # 添加节点数列
        all_data.append(data)

    # 合并所有数据
    df = pd.concat(all_data)

    titles = ['10KB','10MB',"1GB",'10GB','100GB']
    i = 0
    # 按datasize分组生成多张图
    for data_size in df['data_size'].unique():
        fig, ax = plt.subplots(figsize=FIGURE_SIZE2)

        # 筛选特定datasize的数据
        subset = df[df['data_size'] == data_size]

        # 按节点数排序
        subset = subset.sort_values('size')

        # 绘图参数
        x = range(len(Sizes))

        # 绘制柱状图
        rects1 = ax.bar([i - BAR_WIDTH / 2 for i in x], subset['CBTP_OPT'],
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['CBTP_OPT'], label='CBTP-HO'
                        ,edgecolor = edge_color, linewidth=line_width)
        rects2 = ax.bar([i + BAR_WIDTH / 2 for i in x], subset['FTCO'],
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['FTCO'], label='FTCO'
                        ,edgecolor = edge_color, linewidth=line_width)

        # 标签和标题
        ax.set_xlabel("Number of Nodes", fontsize=font_size)
        ax.set_ylabel("AllReduce \nCompletion Time (s)", fontsize=font_size)
        ax.set_title(f"Data Size: {titles[i]}", fontsize=font_size)
        i += 1

        # X轴刻度设置
        ax.set_xticks(x)
        ax.set_xticklabels(Sizes)

        # 自动调整纵坐标范围
        max_val = max(subset[['CBTP_OPT', 'FTCO']].max())
        ax.set_ylim(0, max_val * 1.2)

        # 网格和标签
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        ax.legend(loc='upper left')

        # 保存文件
        os.makedirs(SaveDir, exist_ok=True)
        SaveFile = f"{SaveDir}Allreduce_data_size_{data_size:.0e}.pdf"
        plt.tight_layout()
        fig.savefig(SaveFile)
        print(SaveFile + ' ==================>>> has been complete')
        plt.close()


# 柱形图
# 横坐标：数据大小
# 纵坐标：Allreduce完成时间
# 方案：FTCO、CBTP_OPT
# 不同节点数对应不同图
def Allreduce_with1f():
    Sizes = [128, 256, 512, 1024]
    for size in Sizes:
        data_list = []
        for n in range(1, 11):
            data_list.append(pd.read_csv(ReadDir + f'Allreduce_with1f_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)

        fig, ax = plt.subplots(figsize=FIGURE_SIZE2)

        x_labels = ['10KB','10MB',"1GB",'10GB','100GB']  # 横坐标的标签
        x = range(len(x_labels))
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']

        # 绘制四组柱状图（每组偏移一个柱宽）
        rects2 = ax.bar([i - 0.5 * BAR_WIDTH for i in x], CBTP_OPT,
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['CBTP_OPT'], label='CBTP-HO'
                        ,edgecolor = edge_color, linewidth=line_width)
        rects3 = ax.bar([i + 0.5 * BAR_WIDTH for i in x], FTCO,
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['FTCO'], label='FTCO'
                        ,edgecolor = edge_color, linewidth=line_width)

        ax.set_xlabel("Data Size", fontsize=font_size2)
        ax.set_ylabel("AllReduce \nCompletion Time (s)", fontsize=font_size2)
        # ax.set_ylim(0, max(FTCO) + 2)

        # 设置纵坐标为对数刻度
        ax.set_yscale('log')

        title = f'Cluster Size = {size}'
        ax.set_title(title, fontsize=font_size2)
        # 设置 x 轴的刻度标签
        plt.xticks(x, x_labels)
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        ax.legend()

        plt.tight_layout()

        if not os.path.exists(SaveDir):
            os.makedirs(SaveDir)
        SaveFile = SaveDir + f"Allreduce_with1f_size{size}" + '.pdf'
        fig.savefig(SaveFile)
        print(SaveFile + ' ==================>>> has been complete')
        plt.close()


def Allreduce_with1f2():
    Sizes = [128, 256, 512, 1024]
    all_data = []
    # 读取所有尺寸的数据
    for size in Sizes:
        data_list = []
        for n in range(1, 11):
            data_list.append(pd.read_csv(ReadDir + f'Allreduce_with1f_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        data['size'] = size
        all_data.append(data)

    # 合并所有数据
    df = pd.concat(all_data)

    titles = ['10KB','10MB',"1GB",'10GB','100GB']  # 横坐标的标签
    i = 0

    # 按 data_size 分组生成多张图
    for data_size in df['data_size'].unique():
        fig, ax = plt.subplots(figsize=FIGURE_SIZE2)

        # 筛选特定 data_size 的数据
        subset = df[df['data_size'] == data_size]

        # 按节点数排序
        subset = subset.sort_values('size')

        # 绘图参数
        x = range(len(Sizes))

        # 绘制柱状图
        rects1 = ax.bar([i - BAR_WIDTH / 2 for i in x], subset['CBTP_OPT'],
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['CBTP_OPT'], label='CBTP-HO'
                        ,edgecolor = edge_color, linewidth=line_width)
        rects2 = ax.bar([i + BAR_WIDTH / 2 for i in x], subset['FTCO'],
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['FTCO'], label='FTCO'
                        ,edgecolor = edge_color, linewidth=line_width)

        # 标签和标题
        ax.set_xlabel("The Number of Node", fontsize=font_size2)
        ax.set_ylabel("Time of Allreduce(s)", fontsize=font_size2)
        ax.set_title(f"Data Size: {titles[i]}", fontsize=font_size2)
        i += 1

        # X 轴刻度设置
        ax.set_xticks(x)
        ax.set_xticklabels(Sizes)

        # 自动调整纵坐标范围
        max_val = max(subset[['CBTP_OPT', 'FTCO']].max())
        ax.set_ylim(0, max_val * 1.2)

        # 网格和标签
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        ax.legend()

        # 保存文件
        os.makedirs(SaveDir, exist_ok=True)
        SaveFile = f"{SaveDir}Allreduce_with1f_data_size_{data_size:.0e}.pdf"
        plt.tight_layout()
        fig.savefig(SaveFile)
        print(SaveFile + ' ==================>>> has been complete')
        plt.close()


# 柱形图
# 横坐标：数据大小
# 纵坐标：Allreduce完成时间
# 方案：FTCO、CBTP_OPT
# 不同节点数对应不同图
def Allreduce_with_serialf():
    Sizes = [128, 256, 512, 1024]
    for size in Sizes:
        data_list = []
        for n in range(1, 11):
            data_list.append(pd.read_csv(ReadDir + f'Allreduce_with_serialf_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)

        fig, ax = plt.subplots(figsize=FIGURE_SIZE)

        x_labels = data['data_size']  # 横坐标的标签
        x = range(len(x_labels))
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']

        # 绘制四组柱状图（每组偏移一个柱宽）
        rects2 = ax.bar([i - 0.5 * BAR_WIDTH for i in x], CBTP_OPT,
                        width=BAR_WIDTH, color=COLOR_DICT['CBTP_OPT'], label='CBTP_OPT')
        rects3 = ax.bar([i + 0.5 * BAR_WIDTH for i in x], FTCO,
                        width=BAR_WIDTH, color=COLOR_DICT['FTCO'], label='FTCO')

        ax.set_xlabel("datasize", fontsize=15)
        ax.set_ylabel("allreduce完成时间", fontsize=15)
        ax.set_ylim(0, max(FTCO) + 2)

        ax.set_title("", fontsize=11)
        # 设置 x 轴的刻度标签
        plt.xticks(x, x_labels)
        ax.grid(True, which='both')
        ax.legend()

        plt.tight_layout()

        if not os.path.exists(SaveDir):
            os.makedirs(SaveDir)
        SaveFile = SaveDir + f"Allreduce_with_serialf_size{size}" + '.pdf'
        fig.savefig(SaveFile)
        print(SaveFile + ' ==================>>> has been complete')
        plt.close()


def Allreduce_with_serialf2():
    Sizes = [128, 256, 512, 1024]
    all_data = []
    # 读取所有尺寸的数据
    for size in Sizes:
        data_list = []
        for n in range(1, 11):
            data_list.append(pd.read_csv(ReadDir + f'Allreduce_with_serialf_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        data['size'] = size
        all_data.append(data)

    # 合并所有数据
    df = pd.concat(all_data)

    titles = ['10KB','10MB',"1GB",'10GB','100GB']  # 横坐标的标签
    i=0

    # 按 data_size 分组生成多张图
    for data_size in df['data_size'].unique():
        fig, ax = plt.subplots(figsize=FIGURE_SIZE2)

        # 筛选特定 data_size 的数据
        subset = df[df['data_size'] == data_size]

        # 按节点数排序
        subset = subset.sort_values('size')

        # 绘图参数
        x = range(len(Sizes))

        # 绘制柱状图
        rects1 = ax.bar([i - BAR_WIDTH / 2 for i in x], subset['CBTP_OPT'],
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['CBTP_OPT'], label='CBTP-HO'
                        ,edgecolor = edge_color, linewidth=line_width)
        rects2 = ax.bar([i + BAR_WIDTH / 2 for i in x], subset['FTCO'],
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['FTCO'], label='FTCO'
                        ,edgecolor = edge_color, linewidth=line_width)

        # 标签和标题
        ax.set_xlabel("Number of Nodes", fontsize=font_size2)
        ax.set_ylabel("AllReduce \nCompletion Time (s)", fontsize=font_size2)
        ax.set_title(f"Data Size: {titles[i]}", fontsize=font_size2)
        i += 1

        # X 轴刻度设置
        ax.set_xticks(x)
        ax.set_xticklabels(Sizes)

        # 自动调整纵坐标范围
        max_val = max(subset[['CBTP_OPT', 'FTCO']].max())
        ax.set_ylim(0, max_val * 1.2)

        # 网格和标签
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        ax.legend(loc = 'upper left')

        # 保存文件
        os.makedirs(SaveDir, exist_ok=True)
        SaveFile = f"{SaveDir}Allreduce_with_serialf_data_size_{data_size:.0e}.pdf"
        plt.tight_layout()
        fig.savefig(SaveFile)
        print(SaveFile + ' ==================>>> has been complete')
        plt.close()


# 柱形图
# 横坐标：数据大小
# 纵坐标：Allreduce完成时间
# 方案：FTCO、CBTP_OPT
# 不同节点数对应不同图
def Allreduce_with2f():
    Sizes = [128, 256, 512, 1024]
    for size in Sizes:
        data_list = []
        for n in range(1, 11):
            data_list.append(pd.read_csv(ReadDir + f'Allreduce_with2f_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)

        fig, ax = plt.subplots(figsize=FIGURE_SIZE2)

        x_labels = ['10KB','10MB',"1GB",'10GB','100GB']  # 横坐标的标签
        x = range(len(x_labels))
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']

        # 绘制四组柱状图（每组偏移一个柱宽）
        rects2 = ax.bar([i - 0.5 * BAR_WIDTH for i in x], CBTP_OPT,
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['CBTP_OPT'], label='CBTP-HO'
                        ,edgecolor = edge_color, linewidth=line_width)
        rects3 = ax.bar([i + 0.5 * BAR_WIDTH for i in x], FTCO,
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['FTCO'], label='FTCO'
                        ,edgecolor = edge_color, linewidth=line_width)

        ax.set_xlabel("Data Size", fontsize=font_size2)
        ax.set_ylabel("AllReduce \nCompletion Time (s)", fontsize=font_size2)
        ax.set_ylim(0, max(FTCO) + 2)

        title = f'Cluster Size = {size}'
        ax.set_title(title, fontsize=font_size2)
        # 设置 x 轴的刻度标签
        plt.xticks(x, x_labels)
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        ax.legend(loc = 'upper left')

        plt.tight_layout()

        if not os.path.exists(SaveDir):
            os.makedirs(SaveDir)
        SaveFile = SaveDir + f"Allreduce_with2f_size{size}" + '.pdf'
        fig.savefig(SaveFile)
        print(SaveFile + ' ==================>>> has been complete')
        plt.close()


def Allreduce_with2f2():
    Sizes = [128, 256, 512, 1024]
    all_data = []
    # 读取所有尺寸的数据
    for size in Sizes:
        data_list = []
        for n in range(1, 11):
            data_list.append(pd.read_csv(ReadDir + f'Allreduce_with2f_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        data['size'] = size
        all_data.append(data)

    # 合并所有数据
    df = pd.concat(all_data)

    # 按 data_size 分组生成多张图
    for data_size in df['data_size'].unique():
        fig, ax = plt.subplots(figsize=(10, 6))

        # 筛选特定 data_size 的数据
        subset = df[df['data_size'] == data_size]

        # 按节点数排序
        subset = subset.sort_values('size')

        # 绘图参数
        x = range(len(Sizes))

        # 绘制柱状图
        rects1 = ax.bar([i - BAR_WIDTH / 2 for i in x], subset['CBTP_OPT'],
                        width=BAR_WIDTH, color=COLOR_DICT['CBTP_OPT'], label='CBTP_OPT')
        rects2 = ax.bar([i + BAR_WIDTH / 2 for i in x], subset['FTCO'],
                        width=BAR_WIDTH, color=COLOR_DICT['FTCO'], label='FTCO')

        # 标签和标题
        ax.set_xlabel("节点数", fontsize=12)
        ax.set_ylabel("耗时 (s)", fontsize=12)
        ax.set_title(f"Data Size: {data_size:.1e}", fontsize=14)

        # X 轴刻度设置
        ax.set_xticks(x)
        ax.set_xticklabels(Sizes)

        # 自动调整纵坐标范围
        max_val = max(subset[['CBTP_OPT', 'FTCO']].max())
        ax.set_ylim(0, max_val * 1.2)

        # 网格和标签
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        ax.legend()

        # 保存文件
        os.makedirs(SaveDir, exist_ok=True)
        SaveFile = f"{SaveDir}Allreduce_with2f_data_size_{data_size:.0e}.pdf"
        plt.tight_layout()
        fig.savefig(SaveFile)
        print(SaveFile + ' ==================>>> has been complete')
        plt.close()


# 柱形图
# 横坐标：数据大小
# 纵坐标：Allreduce完成时间
# 方案：FTCO、CBTP_OPT
# 不同节点数对应不同图
def Allreduce_with_serial2f():
    Sizes = [128, 256, 512, 1024]
    for size in Sizes:
        data_list = []
        for n in range(1, 11):
            data_list.append(pd.read_csv(ReadDir + f'Allreduce_with_serial2f_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)

        fig, ax = plt.subplots(figsize=FIGURE_SIZE)

        x_labels = ['10KB','10MB',"1GB",'10GB','100GB']  # 横坐标的标签
        x = range(len(x_labels))
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']

        # 绘制四组柱状图（每组偏移一个柱宽）
        rects2 = ax.bar([i - 0.5 * BAR_WIDTH for i in x], CBTP_OPT,
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['CBTP_OPT'], label='CBTP_OPT'
                        ,edgecolor = edge_color, linewidth=line_width)
        rects3 = ax.bar([i + 0.5 * BAR_WIDTH for i in x], FTCO,
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['FTCO'], label='FTCO'
                        ,edgecolor = edge_color, linewidth=line_width)

        ax.set_xlabel("Data Size", fontsize=font_size)
        ax.set_ylabel("Time of Allreduce(s)", fontsize=font_size)
        ax.set_ylim(0, max(FTCO) + 2)

        title = f'Cluster Size = {size}'
        ax.set_title(title, fontsize=font_size)
        # 设置 x 轴的刻度标签
        plt.xticks(x, x_labels)
        ax.grid(True, which='both')
        ax.legend()

        plt.tight_layout()

        if not os.path.exists(SaveDir):
            os.makedirs(SaveDir)
        SaveFile = SaveDir + f"Allreduce_with_serial2f_size{size}" + '.pdf'
        fig.savefig(SaveFile)
        print(SaveFile + ' ==================>>> has been complete')
        plt.close()


def Allreduce_with_serial2f2():
    Sizes = [128, 256, 512, 1024]
    all_data = []
    # 读取所有尺寸的数据
    for size in Sizes:
        data_list = []
        for n in range(1, 11):
            data_list.append(pd.read_csv(ReadDir + f'Allreduce_with_serial2f_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        data['size'] = size
        all_data.append(data)

    # 合并所有数据
    df = pd.concat(all_data)

    titles = ['10KB','10MB',"1GB",'10GB','100GB']  # 横坐标的标签
    i=0

    # 按 data_size 分组生成多张图
    for data_size in df['data_size'].unique():
        fig, ax = plt.subplots(figsize=FIGURE_SIZE2)

        # 筛选特定 data_size 的数据
        subset = df[df['data_size'] == data_size]

        # 按节点数排序
        subset = subset.sort_values('size')

        # 绘图参数
        x = range(len(Sizes))

        # 绘制柱状图
        rects1 = ax.bar([i - BAR_WIDTH / 2 for i in x], subset['CBTP_OPT'],
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['CBTP_OPT'], label='CBTP-HO'
                        ,edgecolor = edge_color, linewidth=line_width)
        rects2 = ax.bar([i + BAR_WIDTH / 2 for i in x], subset['FTCO'],
                        width=BAR_WIDTH * 0.7, color=COLOR_DICT['FTCO'], label='FTCO'
                        ,edgecolor = edge_color, linewidth=line_width)

        # 标签和标题
        ax.set_xlabel("Number of Nodes", fontsize=font_size2)
        ax.set_ylabel("AllReduce \nCompletion Time (s)", fontsize=font_size2)
        ax.set_title(f"Data Size: {titles[i]}", fontsize=font_size2)
        i += 1

        # X 轴刻度设置
        ax.set_xticks(x)
        ax.set_xticklabels(Sizes)

        # 自动调整纵坐标范围
        max_val = max(subset[['CBTP_OPT', 'FTCO']].max())
        ax.set_ylim(0, max_val * 1.2)

        # 网格和标签
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        ax.legend(loc = 'upper left')

        # 保存文件
        os.makedirs(SaveDir, exist_ok=True)
        SaveFile = f"{SaveDir}Allreduce_with_serial2f_data_size_{data_size:.0e}.pdf"
        plt.tight_layout()
        fig.savefig(SaveFile)
        print(SaveFile + ' ==================>>> has been complete')
        plt.close()


# 折线图
# 横坐标：故障数
# 纵坐标：重建连接数
# 方案：FTCO、CBTP、CBTP_OPT
# 不同节点数对应不同图
def rewirdlinks_withf():
    Sizes = [128, 256, 512, 1024]
    for size in Sizes:
        data_list = []
        for n in range(1, 11):
            data_list.append(pd.read_csv(ReadDir + f'rewiredlinks_withf_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        fig, ax = plt.subplots(figsize=FIGURE_SIZE2)

        x = range(size)
        CBTP = data['CBTP']
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']

        ax.plot(x, CBTP, label='CBTP', linestyle=LINE_STYLES['CBTP'][0], color=COLOR_DICT_LINE['CBTP'])
        ax.plot(x, CBTP_OPT, label='CBTP-HO', linestyle=LINE_STYLES['CBTP_OPT'][0], color=COLOR_DICT_LINE['CBTP_OPT'])
        ax.plot(x, FTCO, label='FTCO', linestyle=LINE_STYLES['FTCO'][0], color=COLOR_DICT_LINE['FTCO'])

        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.set_ylabel('Rewired Link Count', fontsize=font_size2)
        ax.set_xlabel('Number of Leave Nodes', fontsize=font_size2)
        ax.set_ylim(0, max(CBTP_OPT) + 2)
        ax.set_xlim(0, size)
        title = f'Cluster Size = {size}'
        ax.set_title(title, fontsize=font_size2)
        ax.grid(True, which='both')
        ax.legend()
        ax.set_axisbelow(True)

        plt.tight_layout()

        if not os.path.exists(SaveDir):
            os.makedirs(SaveDir)
        SaveFile = SaveDir + f"rewiredlinks_withf_size{size}" + '.pdf'
        fig.savefig(SaveFile)
        print(SaveFile + ' ==================>>> has been complete')
        plt.close()


# 折线图
# 横坐标：故障数
# 纵坐标：带宽比值（CBTP_OPT/FTCO）
# 方案：FTCO、CBTP、CBTP_OPT、新建二叉树
# 不同节点数对应不同图
def bandwidth_withf():
    Sizes = [128, 256, 512, 1024]
    for size in Sizes:
        data_list = []
        for n in range(1, 11):
            data_list.append(pd.read_csv(ReadDir + f'bandwidth_withf_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        fig, ax = plt.subplots(figsize=FIGURE_SIZE2)

        x = range(size)

        FTCO = data['FTCO']
        result = []
        for data in FTCO:
            result.append(FTCO[0] * 2 / data)

        ax.plot(x, result, label='FTCO', linestyle=LINE_STYLES['FTCO'][0], color=COLOR_DICT_LINE['FTCO'])

        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.set_xlabel("Number of Leave Nodes", fontsize=font_size)
        ax.set_ylabel("Bandwidth Ratio", fontsize=font_size)
        ax.set_ylim(0, max(result) + 2)
        ax.set_xlim(0, size)
        title = f'Cluster Size = {size}'
        ax.set_title(title, fontsize=font_size)
        ax.grid(True, which='both')
        ax.set_axisbelow(True)

        plt.tight_layout()

        if not os.path.exists(SaveDir):
            os.makedirs(SaveDir)
        SaveFile = SaveDir + f"bandwidth_withf_size{size}" + '.pdf'
        fig.savefig(SaveFile)
        print(SaveFile + ' ==================>>> has been complete')
        plt.close()

def rewirdlinks_withf2():
    fig, ax = plt.subplots(figsize=FIGURE_SIZE2)
    # 节点数数组
    Sizes = [128, 256, 512, 1024]

    # 计算各方案的比例列表
    r_ftco_list = [1 / (n - 1) for n in Sizes]
    r_cbtp_list = [2 / (n - 1) for n in Sizes]
    r_cbtp_opt_list = [4 / (n - 1) for n in Sizes]

    # 柱状图宽度
    bar_width = 0.2

    # 绘制柱状图
    ax.bar([i - bar_width for i in range(len(Sizes))], r_ftco_list, width=bar_width, label='FTCO', color=COLOR_DICT['FTCO']
            ,edgecolor = edge_color, linewidth=line_width)
    ax.bar([i for i in range(len(Sizes))], r_cbtp_list, width=bar_width, label='CBTP', color=COLOR_DICT['CBTP']
            ,edgecolor = edge_color, linewidth=line_width)
    ax.bar([i + bar_width for i in range(len(Sizes))], r_cbtp_opt_list, width=bar_width, label='CBTP-HO', color=COLOR_DICT['CBTP_OPT']
            ,edgecolor = edge_color, linewidth=line_width)


    # 添加标签和标题
    ax.set_ylim(0,0.05)
    ax.set_xlabel('Number of Nodes',fontsize=font_size2)
    ax.set_ylabel('Ratio of Rewired Links',fontsize=font_size2)
    # plt.title('Ratio of Rewired Links vs The Number of Node')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    ax.set_xticks(range(len(Sizes)))
    ax.set_xticklabels(Sizes)

    # 添加图例
    ax.legend(loc = 'upper right')

    plt.tight_layout()

    if not os.path.exists(SaveDir):
        os.makedirs(SaveDir)
    SaveFile = SaveDir + f"rewiredlinks" + '.pdf'
    fig.savefig(SaveFile)
    print(SaveFile + ' ==================>>> has been complete')
    plt.close()

def rewired_time():
    rewired_times = [0.0, 0.1, 0.5, 1.0, 2.0 ,5.0 , 10.0, 20.0, 30.0, 60.0, 120.0]
    size =  512
    data_size = 100000000000.0
    cbtp_opt_times = []
    ftco_times = []
    for rewired_time in rewired_times:
        dir = f'/home/sx/double_tree/double_tree/result_bandwith{Network.bandwidth}_rewiredtime{rewired_time}_timestep{Network.time_step}_latency{Network.latency}/'
        data_list = []
        for n in range(1, 11):
            data_list.append(pd.read_csv(dir + f'Allreduce_with_serialf_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        filtered_data = data[data['data_size'] == data_size]
        cbtp_opt_times.append(filtered_data['CBTP_OPT'].values[0])
        ftco_times.append(filtered_data['FTCO'].values[0])
    fig, ax = plt.subplots(figsize=FIGURE_SIZE2)

    x_labels = [0.0, 0.1, 0.5, 1.0, 2.0 ,5.0 , 10, 20, 30, 60, 120]  # 横坐标的标签
    x = range(len(rewired_times))

    # 绘制四组柱状图（每组偏移一个柱宽）
    rects2 = ax.bar([i - 0.5 * BAR_WIDTH for i in x], cbtp_opt_times,
                    width=BAR_WIDTH, color=COLOR_DICT['CBTP_OPT'], label='CBTP-HO'
                    ,edgecolor = edge_color, linewidth=line_width)
    rects3 = ax.bar([i + 0.5 * BAR_WIDTH for i in x], ftco_times,
                    width=BAR_WIDTH, color=COLOR_DICT['FTCO'], label='FTCO'
                    ,edgecolor = edge_color, linewidth=line_width)

    ax.set_xlabel("Rewired Time (s)", fontsize=font_size2)
    ax.set_ylabel("AllReduce \nCompletion Time (s)", fontsize=font_size2)
    ax.set_ylim(0, max(ftco_times) + 2)

    # ax.set_title("", fontsize=11)
    # 设置 x 轴的刻度标签
    plt.xticks(x, x_labels)
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    ax.legend()

    plt.tight_layout()

    if not os.path.exists(SaveDir):
        os.makedirs(SaveDir)
    SaveFile = SaveDir + f"rewiredtime_size{size}_datasize{data_size}" + '.pdf'
    fig.savefig(SaveFile)
    print(SaveFile + ' ==================>>> has been complete')
    plt.close()



# 在每个柱子上标上数字
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        plt.annotate('{}'.format(height),
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),  # 3 点垂直偏移量
                     textcoords="offset points",
                     ha='center', va='bottom')


if __name__ == '__main__':

    time = float(sys.argv[1])
    Network.rewired_time = time

    ReadDir = f'/home/sx/double_tree/double_tree/result_bandwith{Network.bandwidth}_rewiredtime{Network.rewired_time}_timestep{Network.time_step}_latency{Network.latency}/'
    SaveDir = f'./pictures_bandwith{Network.bandwidth}_rewiredtime{Network.rewired_time}_timestep{Network.time_step}_latency{Network.latency}/'


    # height_nof()
    # height_withf()
    # Allreduce_with1f()
    # Allreduce_with_serialf()
    # Allreduce_with2f()
    # Allreduce_with_serial2f()
    # rewirdlinks_withf()
    # bandwidth_withf()
    # Allreduce_nof()
    # Allreduce_nof2()
    # Allreduce_with1f2()
    # Allreduce_with_serialf2()
    # Allreduce_with2f2()
    # Allreduce_with_serial2f2()
    # rewirdlinks_withf2()
    rewired_time()