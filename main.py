from CBTP import CBTP as CBTP
from CBTP_OPT import CBTP_OPT as CBTP_OPT
from FTCO import FTCO
from core import Network,Event,SimulationKernel,AllreduceEvent
from CBTP_sim import CBTPNodeLeaveEvent as CBTPLE, CBTPNodeLeaveCompletedEvent as CBTPLCE, CBTPNodeJoinEvent as CBTPJE, CBTPNodeJoinCompletedEvent as CBTPJCE
from FTCO_sim import FTCONodeLeaveEvent as FTCOLE, FTCONodeLeaveCompletedEvent as FTCOLCE
import sys
import random
import math
import time
import csv
import os

SaveDir = f'./result_bandwith{Network.bandwidth}_rewiredtime{Network.rewired_time}_timestep{Network.time_step}_latency{Network.latency}/'

# 创建目录（如果目录不存在）
if not os.path.exists(SaveDir):
    os.makedirs(SaveDir)
    print(f"目录已创建: {SaveDir}")
else:
    print(f"目录已存在: {SaveDir}")

# 测试场景：无故障场景
# 测试指标：树高
# 对比方案：FTCO、CBTP、CBTP_OPT、新建二叉树
# 变量：节点数
# 证明在无故障时对于小消息传输CBTP很高效
def height_nof():
    Sizes = [8,16,32,64,128,256,512,1024]
    Title = ["Node_num","CBTP","CBTP_OPT","FTCO","binary_tree"] 
    Data = [[0] * len(Title) for _ in range(len(Sizes))]
    for i in range(len(Sizes)):
        Size = Sizes[i]
        cbtp = CBTP(Size)
        cbtp_OPT = CBTP_OPT(Size)
        ftco = FTCO(Size)
        Data[i][0] = Size
        Data[i][1] = cbtp.height
        Data[i][2] = cbtp_OPT.height
        Data[i][3] = ftco.height
        Data[i][4] = math.floor(math.log2(Size))

    with open(SaveDir + "height_nof.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(Title)
        writer.writerows(Data)

# 测试场景：有故障场景
# 测试指标：树高
# 对比方案：FTCO、CBTP、CBTP_OPT、新建二叉树
# 变量：节点数、故障数
# 证明在有故障时对于小消息传输CBTP很高效
def height_withf():
    Sizes = [128,256,512,1024]
    Title = ["CBTP","CBTP_OPT","FTCO","binary_tree"] 

    Data = [0]*len(Title)
    for num in range(1,11):
        for Size in Sizes:
            cbtp = CBTP(Size)
            cbtp_OPT = CBTP_OPT(Size)
            ftco = FTCO(Size)

            with open(SaveDir + f"height_withf_size{Size}_{num}.csv", "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(Title)
            
            eraseNodes = [i for i in range(Size)]
            random.shuffle(eraseNodes)

            for eraseNode in eraseNodes:
                Data[0] = cbtp.height
                Data[1] = cbtp_OPT.height
                Data[2] = ftco.height
                Data[3] = math.floor(math.log2(ftco.size))
                with open(SaveDir + f"height_withf_size{Size}_{num}.csv", "a", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(Data)
                cbtp_OPT.erase_node(eraseNode)
                cbtp.erase_node(eraseNode)
                ftco.erase_node(eraseNode)


# 测试场景：无故障场景
# 测试指标：Allreduce完成时间
# 对比方案：FTCO、CBTP 
# 变量：节点数、消息大小
def Allreduce_nof():
    Sizes = [128,256,512,1024]
    datas = [10e3, 10e6, 10e9, 100e9, 1e12]  # 数据大小单位KB
    Title = ["data_size", "CBTP_OPT",  "FTCO"] 
    Data = [0]*len(Title)
    for Size in Sizes:
        with open(SaveDir + f"Allreduce_nof_size{Size}.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(Title)
        for data in datas:
            cbtp_OPT = CBTP_OPT(Size)
            ftco = FTCO(Size, Network.bandwidth)
            sim_CBTP = SimulationKernel(cbtp_OPT)
            sim_FTCO = SimulationKernel(ftco)
            sim_FTCO.current_bandwidth = Network.bandwidth/2  # 一棵树只用了一半的带宽

            sim_CBTP.schedule(AllreduceEvent(start_time=0, data_size=data))
            sim_FTCO.schedule(AllreduceEvent(start_time=0, data_size=data))
            sim_CBTP.run()
            sim_FTCO.run()
            Data[0] = data
            Data[1] = sim_CBTP.stats['completed_times'][0]
            Data[2] = sim_FTCO.stats['completed_times'][0]
            with open(SaveDir + f"Allreduce_nof_size{Size}.csv", "a", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(Data)


# 测试场景：单点故障场景
# 测试指标：Allreduce完成时间
# 对比方案：FTCO、CBTP 
# 变量：节点数、消息大小
# CBTP在单点故障时依然有一棵树可用，使得小消息完成更快, 大消息也有提升
def Allreduce_with1f():
    Sizes = [128,256,512,1024]
    datas = [10e3, 10e6, 10e9, 100e9, 1e12]  # 数据大小单位KB
    Title = ["data_size", "CBTP_OPT",  "FTCO"] 
    Data = [0]*len(Title)
    for num in range(1,11):
        for Size in Sizes:
            with open(SaveDir + f"Allreduce_with1f_size{Size}_{num}.csv", "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(Title)
            for data in datas:
                cbtp_OPT = CBTP_OPT(Size)
                ftco = FTCO(Size, Network.bandwidth)
                sim_CBTP = SimulationKernel(cbtp_OPT)
                sim_FTCO = SimulationKernel(ftco)
                sim_FTCO.current_bandwidth = Network.bandwidth/2  # 一棵树只用了一半的带宽

                sim_CBTP.schedule(AllreduceEvent(start_time=0, data_size=data))
                sim_FTCO.schedule(AllreduceEvent(start_time=0, data_size=data))

                eraseNodes = [i for i in range(Size)]
                random.shuffle(eraseNodes)

                for eraseNode in eraseNodes:
                    sim_CBTP.schedule(CBTPLE(timestamp=sim_CBTP.current_time, leave_id=eraseNode))
                    sim_FTCO.schedule(FTCOLE(timestamp=sim_FTCO.current_time, leave_id=eraseNode))
                    sim_CBTP.run()
                    sim_FTCO.run()
                    Data[0] = data
                    Data[1] = sim_CBTP.stats['completed_times'][0]
                    Data[2] = sim_FTCO.stats['completed_times'][0]
                    with open(SaveDir + f"Allreduce_with1f_size{Size}_{num}.csv", "a", newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(Data)
                    break


# 测试场景：连续单点故障场景
# 测试指标：Allreduce完成时间
# 对比方案：FTCO、CBTP 
# 变量：节点数、消息大小
# CBTP在连续单点故障时依然有一棵树可用，使得小消息完成更快, 大消息也有提升
def Allreduce_with_serialf():
    Sizes = [128,256,512,1024]
    datas = [10e3, 10e6, 10e9, 100e9, 1e12]  # 数据大小单位KB
    Title = ["data_size", "CBTP_OPT",  "FTCO"] 
    Data = [0]*len(Title)
    for num in range(1,11):
        for Size in Sizes:
            with open(SaveDir + f"Allreduce_with_serialf_size{Size}_{num}.csv", "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(Title)
            for data in datas:
                cbtp_OPT = CBTP_OPT(Size)
                ftco = FTCO(Size, Network.bandwidth)
                sim_CBTP = SimulationKernel(cbtp_OPT)
                sim_FTCO = SimulationKernel(ftco)
                sim_FTCO.current_bandwidth = Network.bandwidth/2  # 一棵树只用了一半的带宽

                sim_CBTP.schedule(AllreduceEvent(start_time=0, data_size=data))
                sim_FTCO.schedule(AllreduceEvent(start_time=0, data_size=data))

                eraseNodes = [i for i in range(Size)]
                random.shuffle(eraseNodes)
                
                # 注入10倍数据的Allreduce任务
                # 每25s注入一个故障
                sim_CBTP.schedule(AllreduceEvent(start_time=0, data_size=data*10))
                sim_FTCO.schedule(AllreduceEvent(start_time=0, data_size=data*10))
                count = 0
                for eraseNode in eraseNodes:

                    sim_CBTP.schedule(CBTPLE(timestamp=sim_CBTP.current_time + count * (Network.rewired_time + 5), leave_id=eraseNode))
                    sim_FTCO.schedule(FTCOLE(timestamp=sim_FTCO.current_time + count * (Network.rewired_time + 5), leave_id=eraseNode))
                    count += 1
                    if count == 10:
                        break
                sim_CBTP.run()
                sim_FTCO.run()
                Data[0] = data
                Data[1] = max(sim_CBTP.stats['completed_times'])
                Data[2] = max(sim_FTCO.stats['completed_times'])
                with open(SaveDir + f"Allreduce_with_serialf_size{Size}_{num}.csv", "a", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(Data)

# 测试场景：并发故障场景
# 测试指标：Allreduce完成时间
# 对比方案：FTCO、CBTP 
# 变量：节点数、消息大小
# CBTP在两棵树同时被破坏时拥有跟FTCO一样的恢复时间
def Allreduce_with2f():
    Sizes = [128,256,512,1024]
    datas = [10e3, 10e6, 10e9, 100e9, 1e12]  # 数据大小单位KB
    Title = ["data_size", "CBTP_OPT",  "FTCO"] 
    Data = [0]*len(Title)
    for num in range(1,11):
        for Size in Sizes:
            with open(SaveDir + f"Allreduce_with2f_size{Size}_{num}.csv", "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(Title)
            for data in datas:
                cbtp_OPT = CBTP_OPT(Size)
                ftco = FTCO(Size, Network.bandwidth)
                sim_CBTP = SimulationKernel(cbtp_OPT)
                sim_FTCO = SimulationKernel(ftco)
                sim_FTCO.current_bandwidth = Network.bandwidth/2  # 一棵树只用了一半的带宽

                sim_CBTP.schedule(AllreduceEvent(start_time=0, data_size=data))
                sim_FTCO.schedule(AllreduceEvent(start_time=0, data_size=data))

                eraseNodes = [i for i in range(Size)]
                random.shuffle(eraseNodes)

                count = 0
                for eraseNode in eraseNodes:
                    sim_CBTP.schedule(CBTPLE(timestamp=sim_CBTP.current_time, leave_id=eraseNode))
                    sim_FTCO.schedule(FTCOLE(timestamp=sim_FTCO.current_time, leave_id=eraseNode))
                    count += 1
                    if count == 2:
                        break
                sim_CBTP.run()
                sim_FTCO.run()
                Data[0] = data
                Data[1] = sim_CBTP.stats['completed_times'][0]
                Data[2] = sim_FTCO.stats['completed_times'][0]
                with open(SaveDir + f"Allreduce_with2f_size{Size}_{num}.csv", "a", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(Data)

# 测试场景：连续并发故障场景
# 测试指标：Allreduce完成时间
# 对比方案：FTCO、CBTP 
# 变量：节点数、消息大小
# CBTP在连续并发故障时恢复与FTCO一致，但恢复后拥有更好的树结构
def Allreduce_with_serial2f():
    Sizes = [128,256,512,1024]
    datas = [10e3, 10e6, 10e9, 100e9, 1e12]  # 数据大小单位KB
    Title = ["data_size", "CBTP_OPT",  "FTCO"] 
    Data = [0]*len(Title)
    for num in range(1,11):
        for Size in Sizes:
            with open(SaveDir + f"Allreduce_with_serial2f_size{Size}_{num}.csv", "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(Title)
            for data in datas:
                cbtp_OPT = CBTP_OPT(Size)
                ftco = FTCO(Size, Network.bandwidth)
                sim_CBTP = SimulationKernel(cbtp_OPT)
                sim_FTCO = SimulationKernel(ftco)
                sim_FTCO.current_bandwidth = Network.bandwidth/2  # 一棵树只用了一半的带宽

                sim_CBTP.schedule(AllreduceEvent(start_time=0, data_size=data))
                sim_FTCO.schedule(AllreduceEvent(start_time=0, data_size=data))

                eraseNodes = [i for i in range(Size)]
                random.shuffle(eraseNodes)
                
                # 每20s注入一个Allreduce任务
                # 每25s注入两个故障
                sim_CBTP.schedule(AllreduceEvent(start_time=0, data_size=data*10))
                sim_FTCO.schedule(AllreduceEvent(start_time=0, data_size=data*10))
      
                i = 0
                count = 0
                while(count < 10):
                    sim_CBTP.schedule(CBTPLE(timestamp=sim_CBTP.current_time + count * (Network.rewired_time + 5), leave_id=eraseNodes[i]))
                    sim_CBTP.schedule(CBTPLE(timestamp=sim_CBTP.current_time + count * (Network.rewired_time + 5), leave_id=eraseNodes[i+1]))
                    sim_FTCO.schedule(FTCOLE(timestamp=sim_FTCO.current_time + count * (Network.rewired_time + 5), leave_id=eraseNodes[i]))
                    sim_FTCO.schedule(FTCOLE(timestamp=sim_FTCO.current_time + count * (Network.rewired_time + 5), leave_id=eraseNodes[i+1]))
                    count += 1
                    i += 2
                sim_CBTP.run()
                sim_FTCO.run()
                Data[0] = data
                Data[1] = max(sim_CBTP.stats['completed_times'])
                Data[2] = max(sim_FTCO.stats['completed_times'])
                with open(SaveDir + f"Allreduce_with_serial2f_size{Size}_{num}.csv", "a", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(Data)

# 测试场景：有故障场景
# 测试指标：重建链接数
# 对比方案：FTCO、CBTP、CBTP_OPT
# 变量：节点数、故障数
def rewirdlinks_withf():
    Sizes = [128,256,512,1024]
    Title = ["CBTP","CBTP_OPT","FTCO"] 

    Data = [0]*len(Title)
    for num in range(1,11):
        for Size in Sizes:
            cbtp = CBTP(Size)
            cbtp_OPT = CBTP_OPT(Size)
            ftco = FTCO(Size)

            with open(SaveDir + f"rewiredlinks_withf_size{Size}_{num}.csv", "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(Title)
            
            eraseNodes = [i for i in range(Size)]
            random.shuffle(eraseNodes)

            for eraseNode in eraseNodes:
                Data[0] = cbtp.rewired_links
                Data[1] = cbtp_OPT.rewired_links
                Data[2] = ftco.rewired_links
                with open(SaveDir + f"rewiredlinks_withf_size{Size}_{num}.csv", "a", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(Data)
                cbtp_OPT.erase_node(eraseNode)
                cbtp.erase_node(eraseNode)
                ftco.erase_node(eraseNode)

# 测试场景：有故障场景
# 测试指标：带宽对比
# 对比方案：FTCO、CBTP_OPT
# 变量：节点数、故障数
def bandwidth_withf():
    Sizes = [128,256,512,1024]
    Title = ["FTCO"] 

    Data = [0]*len(Title)
    for num in range(1,11):
        for Size in Sizes:
            ftco = FTCO(Size, Network.bandwidth)

            with open(SaveDir + f"bandwidth_withf_size{Size}_{num}.csv", "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(Title)
            
            eraseNodes = [i for i in range(Size)]
            random.shuffle(eraseNodes)

            for eraseNode in eraseNodes:
                Data[0] = ftco.bandwidth
                with open(SaveDir + f"bandwidth_withf_size{Size}_{num}.csv", "a", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(Data)
                ftco.erase_node(eraseNode)

if __name__ == "__main__" :
    height_nof()
    bandwidth_withf()
    height_withf()
    Allreduce_nof()
    Allreduce_with1f()
    Allreduce_with_serialf()
    Allreduce_with2f()
    Allreduce_with_serial2f()
    rewirdlinks_withf()
    
    # pass