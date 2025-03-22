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
    data = pd.read_csv( ReadDir + 'height_nof.csv')
    fig, ax = plt.subplots(figsize=(8, 6))

    bar_width = 0.2
    x_labels = data['Node_num']  # 横坐标的标签
    x = range(len(x_labels))
    CBTP = data['CBTP']
    CBTP_OPT = data['CBTP_OPT']
    FTCO = data['FTCO']
    binary_tree = data['binary_tree']

    # 定义颜色方案
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    # 绘制四组柱状图（每组偏移一个柱宽）
    rects1 = ax.bar([i - 1.5*bar_width for i in x], CBTP, 
                   width=bar_width, color=colors[0], label='CBTP')
    rects2 = ax.bar([i - 0.5*bar_width for i in x], CBTP_OPT, 
                   width=bar_width, color=colors[1], label='CBTP_OPT')
    rects3 = ax.bar([i + 0.5*bar_width for i in x], FTCO, 
                   width=bar_width, color=colors[2], label='FTCO')
    rects4 = ax.bar([i + 1.5*bar_width for i in x], binary_tree, 
                   width=bar_width, color=colors[3], label='Binary Tree')

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    ax.set_xlabel("节点数", fontsize = 15)
    ax.set_ylabel("树高", fontsize = 15)
    ax.set_ylim(0, 11)

    ax.set_title("", fontsize=11)
    # 设置 x 轴的刻度标签
    plt.xticks(x, x_labels)
    ax.grid(True, which='both')
    ax.legend()
    
    # add_labels(bars1)
    # add_labels(bars2)

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
    Sizes = [128,256,512,1024]
    for size in Sizes:
        data_list = []
        for n in range(1,11):
            data_list.append(pd.read_csv(ReadDir + f'height_withf_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        fig, ax = plt.subplots(figsize=(8, 6))

        x = range(size)
        CBTP = data['CBTP']
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']
        binary_tree = data['binary_tree']

        styles = {
            'CBTP': ['-'], 
            'CBTP_OPT': ['--'],  # 虚线
            'FTCO': [':'],  # 点线
            'binary_tree': ['-.']  # 双点划线
        }
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

        ax.plot(x, CBTP, label='CBTP', linestyle=styles['CBTP'][0], color=colors[0])
        ax.plot(x, CBTP_OPT, label='CBTP_OPT', linestyle=styles['CBTP_OPT'][0], color=colors[1])
        ax.plot(x, FTCO, label='FTCO', linestyle=styles['FTCO'][0], color=colors[2])
        ax.plot(x, binary_tree, label='binary_tree', linestyle=styles['binary_tree'][0], color=colors[3])

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.set_xlabel("节点数", fontsize = 15)
        ax.set_ylabel("树高", fontsize = 15)
        ax.set_ylim(0,max(CBTP) + 2)
        ax.set_xlim(0,size)
        ax.set_title("", fontsize=17)
        ax.grid(True, which='both')
        ax.legend()
        ax.set_axisbelow(True)
        # for spine in ax.spines.values():
        #     spine.set_zorder(10)
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
    Sizes = [128,256,512,1024]
    for size in Sizes:
        data = pd.read_csv(ReadDir + f'Allreduce_nof_size{size}.csv')

        
        fig, ax = plt.subplots(figsize=(8, 6))

        bar_width = 0.3
        x_labels = data['data_size']  # 横坐标的标签
        x = range(len(x_labels))
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']

        # 定义颜色方案
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        # 绘制四组柱状图（每组偏移一个柱宽）
        rects2 = ax.bar([i - 0.5*bar_width for i in x], CBTP_OPT, 
                    width=bar_width, color=colors[1], label='CBTP_OPT')
        rects3 = ax.bar([i + 0.5*bar_width for i in x], FTCO, 
                    width=bar_width, color=colors[2], label='FTCO')

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        ax.set_xlabel("datasize", fontsize = 15)
        ax.set_ylabel("allreduce完成时间", fontsize = 15)
        ax.set_ylim(0, max(FTCO)+2)

        ax.set_title("", fontsize=11)
        # 设置 x 轴的刻度标签
        plt.xticks(x, x_labels)
        ax.grid(True, which='both')
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
    
    # 按datasize分组生成多张图
    for data_size in df['data_size'].unique():
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 筛选特定datasize的数据
        subset = df[df['data_size'] == data_size]
        
        # 按节点数排序
        subset = subset.sort_values('size')
        
        # 绘图参数
        bar_width = 0.35
        x = range(len(Sizes))
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        # 绘制柱状图
        rects1 = ax.bar([i - bar_width/2 for i in x], subset['CBTP_OPT'], 
                       width=bar_width, color=colors[1], label='CBTP_OPT')
        rects2 = ax.bar([i + bar_width/2 for i in x], subset['FTCO'], 
                       width=bar_width, color=colors[2], label='FTCO')
        
        # 设置中文显示
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        
        # 标签和标题
        ax.set_xlabel("节点数", fontsize=12)
        ax.set_ylabel("耗时 (ms)", fontsize=12)
        ax.set_title(f"Data Size: {data_size:.1e}", fontsize=14)
        
        # X轴刻度设置
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
    Sizes = [128,256,512,1024]
    for size in Sizes:
        data_list = []
        for n in range(1,11):
            data_list.append(pd.read_csv(ReadDir + f'Allreduce_with1f_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        
        fig, ax = plt.subplots(figsize=(8, 6))

        bar_width = 0.3
        x_labels = data['data_size']  # 横坐标的标签
        x = range(len(x_labels))
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']

        # 定义颜色方案
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        # 绘制四组柱状图（每组偏移一个柱宽）
        rects2 = ax.bar([i - 0.5*bar_width for i in x], CBTP_OPT, 
                    width=bar_width, color=colors[1], label='CBTP_OPT')
        rects3 = ax.bar([i + 0.5*bar_width for i in x], FTCO, 
                    width=bar_width, color=colors[2], label='FTCO')

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        ax.set_xlabel("datasize", fontsize = 15)
        ax.set_ylabel("allreduce完成时间", fontsize = 15)
        ax.set_ylim(0, max(FTCO)+2)

        ax.set_title("", fontsize=11)
        # 设置 x 轴的刻度标签
        plt.xticks(x, x_labels)
        ax.grid(True, which='both')
        ax.legend()
        
        # add_labels(bars1)
        # add_labels(bars2)

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

    # 按 data_size 分组生成多张图
    for data_size in df['data_size'].unique():
        fig, ax = plt.subplots(figsize=(10, 6))

        # 筛选特定 data_size 的数据
        subset = df[df['data_size'] == data_size]

        # 按节点数排序
        subset = subset.sort_values('size')

        # 绘图参数
        bar_width = 0.35
        x = range(len(Sizes))
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

        # 绘制柱状图
        rects1 = ax.bar([i - bar_width / 2 for i in x], subset['CBTP_OPT'],
                        width=bar_width, color=colors[1], label='CBTP_OPT')
        rects2 = ax.bar([i + bar_width / 2 for i in x], subset['FTCO'],
                        width=bar_width, color=colors[2], label='FTCO')

        # 设置中文显示
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

        # 标签和标题
        ax.set_xlabel("节点数", fontsize=12)
        ax.set_ylabel("耗时 (ms)", fontsize=12)
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
    Sizes = [128,256,512,1024]
    for size in Sizes:
        data_list = []
        for n in range(1,11):
            data_list.append(pd.read_csv(ReadDir + f'Allreduce_with_serialf_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        
        fig, ax = plt.subplots(figsize=(8, 6))

        bar_width = 0.3
        x_labels = data['data_size']  # 横坐标的标签
        x = range(len(x_labels))
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']

        # 定义颜色方案
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        # 绘制四组柱状图（每组偏移一个柱宽）
        rects2 = ax.bar([i - 0.5*bar_width for i in x], CBTP_OPT, 
                    width=bar_width, color=colors[1], label='CBTP_OPT')
        rects3 = ax.bar([i + 0.5*bar_width for i in x], FTCO, 
                    width=bar_width, color=colors[2], label='FTCO')

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        ax.set_xlabel("datasize", fontsize = 15)
        ax.set_ylabel("allreduce完成时间", fontsize = 15)
        ax.set_ylim(0, max(FTCO)+2)

        ax.set_title("", fontsize=11)
        # 设置 x 轴的刻度标签
        plt.xticks(x, x_labels)
        ax.grid(True, which='both')
        ax.legend()
        
        # add_labels(bars1)
        # add_labels(bars2)

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

    # 按 data_size 分组生成多张图
    for data_size in df['data_size'].unique():
        fig, ax = plt.subplots(figsize=(10, 6))

        # 筛选特定 data_size 的数据
        subset = df[df['data_size'] == data_size]

        # 按节点数排序
        subset = subset.sort_values('size')

        # 绘图参数
        bar_width = 0.35
        x = range(len(Sizes))
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

        # 绘制柱状图
        rects1 = ax.bar([i - bar_width / 2 for i in x], subset['CBTP_OPT'],
                        width=bar_width, color=colors[1], label='CBTP_OPT')
        rects2 = ax.bar([i + bar_width / 2 for i in x], subset['FTCO'],
                        width=bar_width, color=colors[2], label='FTCO')

        # 设置中文显示
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

        # 标签和标题
        ax.set_xlabel("节点数", fontsize=12)
        ax.set_ylabel("耗时 (ms)", fontsize=12)
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
    Sizes = [128,256,512,1024]
    for size in Sizes:
        data_list = []
        for n in range(1,11):
            data_list.append(pd.read_csv(ReadDir + f'Allreduce_with2f_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        
        fig, ax = plt.subplots(figsize=(8, 6))

        bar_width = 0.3
        x_labels = data['data_size']  # 横坐标的标签
        x = range(len(x_labels))
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']

        # 定义颜色方案
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        # 绘制四组柱状图（每组偏移一个柱宽）
        rects2 = ax.bar([i - 0.5*bar_width for i in x], CBTP_OPT, 
                    width=bar_width, color=colors[1], label='CBTP_OPT')
        rects3 = ax.bar([i + 0.5*bar_width for i in x], FTCO, 
                    width=bar_width, color=colors[2], label='FTCO')

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        ax.set_xlabel("datasize", fontsize = 15)
        ax.set_ylabel("allreduce完成时间", fontsize = 15)
        ax.set_ylim(0, max(FTCO)+2)

        ax.set_title("", fontsize=11)
        # 设置 x 轴的刻度标签
        plt.xticks(x, x_labels)
        ax.grid(True, which='both')
        ax.legend()
        
        # add_labels(bars1)
        # add_labels(bars2)

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
        bar_width = 0.35
        x = range(len(Sizes))
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

        # 绘制柱状图
        rects1 = ax.bar([i - bar_width / 2 for i in x], subset['CBTP_OPT'],
                        width=bar_width, color=colors[1], label='CBTP_OPT')
        rects2 = ax.bar([i + bar_width / 2 for i in x], subset['FTCO'],
                        width=bar_width, color=colors[2], label='FTCO')

        # 设置中文显示
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

        # 标签和标题
        ax.set_xlabel("节点数", fontsize=12)
        ax.set_ylabel("耗时 (ms)", fontsize=12)
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
    Sizes = [128,256,512,1024]
    for size in Sizes:
        data_list = []
        for n in range(1,11):
            data_list.append(pd.read_csv(ReadDir + f'Allreduce_with_serial2f_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        
        fig, ax = plt.subplots(figsize=(8, 6))

        bar_width = 0.3
        x_labels = data['data_size']  # 横坐标的标签
        x = range(len(x_labels))
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']

        # 定义颜色方案
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        # 绘制四组柱状图（每组偏移一个柱宽）
        rects2 = ax.bar([i - 0.5*bar_width for i in x], CBTP_OPT, 
                    width=bar_width, color=colors[1], label='CBTP_OPT')
        rects3 = ax.bar([i + 0.5*bar_width for i in x], FTCO, 
                    width=bar_width, color=colors[2], label='FTCO')

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        ax.set_xlabel("datasize", fontsize = 15)
        ax.set_ylabel("allreduce完成时间", fontsize = 15)
        ax.set_ylim(0, max(FTCO)+2)

        ax.set_title("", fontsize=11)
        # 设置 x 轴的刻度标签
        plt.xticks(x, x_labels)
        ax.grid(True, which='both')
        ax.legend()
        
        # add_labels(bars1)
        # add_labels(bars2)

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

    # 按 data_size 分组生成多张图
    for data_size in df['data_size'].unique():
        fig, ax = plt.subplots(figsize=(10, 6))

        # 筛选特定 data_size 的数据
        subset = df[df['data_size'] == data_size]

        # 按节点数排序
        subset = subset.sort_values('size')

        # 绘图参数
        bar_width = 0.35
        x = range(len(Sizes))
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

        # 绘制柱状图
        rects1 = ax.bar([i - bar_width / 2 for i in x], subset['CBTP_OPT'],
                        width=bar_width, color=colors[1], label='CBTP_OPT')
        rects2 = ax.bar([i + bar_width / 2 for i in x], subset['FTCO'],
                        width=bar_width, color=colors[2], label='FTCO')

        # 设置中文显示
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

        # 标签和标题
        ax.set_xlabel("节点数", fontsize=12)
        ax.set_ylabel("耗时 (ms)", fontsize=12)
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
    Sizes = [128,256,512,1024]
    for size in Sizes:
        data_list = []
        for n in range(1,11):
            data_list.append(pd.read_csv(ReadDir + f'rewiredlinks_withf_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        fig, ax = plt.subplots(figsize=(8, 6))

        x = range(size)
        CBTP = data['CBTP']
        CBTP_OPT = data['CBTP_OPT']
        FTCO = data['FTCO']

        styles = {
            'CBTP': ['-'], 
            'CBTP_OPT': ['--'],  # 虚线
            'FTCO': [':'],  # 点线
            'binary_tree': ['-.']  # 双点划线
        }
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

        ax.plot(x, CBTP, label='CBTP', linestyle=styles['CBTP'][0], color=colors[0])
        ax.plot(x, CBTP_OPT, label='CBTP_OPT', linestyle=styles['CBTP_OPT'][0], color=colors[1])
        ax.plot(x, FTCO, label='FTCO', linestyle=styles['FTCO'][0], color=colors[2])
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.set_ylabel('重建连接数', fontsize= 15)
        ax.set_xlabel('Number of Departure Node', fontsize= 15)
        ax.set_ylim(0,max(CBTP_OPT) + 2)
        ax.set_xlim(0,size)
        ax.set_title("", fontsize=17)
        ax.grid(True, which='both')
        ax.legend()
        ax.set_axisbelow(True)
        # for spine in ax.spines.values():
        #     spine.set_zorder(10)
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
    Sizes = [128,256,512,1024]
    for size in Sizes:
        data_list = []
        for n in range(1,11):
            data_list.append(pd.read_csv(ReadDir + f'bandwidth_withf_size{size}_{n}.csv'))
        data = sum(data_list) / len(data_list)
        fig, ax = plt.subplots(figsize=(8, 6))

        x = range(size)

        FTCO = data['FTCO']
        result = []
        for data in FTCO:
            result.append(FTCO[0]*2/data)
        
        styles = {
            'CBTP': ['-'], 
            'CBTP_OPT': ['--'],  # 虚线
            'FTCO': [':'],  # 点线
            'binary_tree': ['-.']  # 双点划线
        }
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

        ax.plot(x, result, label='FTCO', linestyle=styles['FTCO'][0], color=colors[2])

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.set_xlabel("故障数", fontsize = 15)
        ax.set_ylabel("带宽比", fontsize = 15)
        ax.set_ylim(0,max(result) + 2)
        ax.set_xlim(0,size)
        ax.set_title("", fontsize=17)
        ax.grid(True, which='both')
        # ax.legend()
        ax.set_axisbelow(True)
        # for spine in ax.spines.values():
        #     spine.set_zorder(10)
        plt.tight_layout()

        if not os.path.exists(SaveDir):
            os.makedirs(SaveDir)
        SaveFile = SaveDir + f"bandwidth_withf_size{size}" + '.pdf'
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

    height_nof()
    height_withf()
    Allreduce_with1f()
    Allreduce_with_serialf()
    Allreduce_with2f()
    Allreduce_with_serial2f()
    rewirdlinks_withf()
    bandwidth_withf()
    Allreduce_nof()
    Allreduce_nof2()
    Allreduce_with1f2()
    Allreduce_with_serialf2()
    Allreduce_with2f2()
    Allreduce_with_serial2f2()
