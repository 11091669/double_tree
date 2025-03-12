from double_tree import double_tree as dbT
from double_tree_OPT import double_tree_OPT as dbT_OPT
from core import Network,Event,SimulationKernel,AllreduceEvent

class CBTPNodeLeaveEvent(Event):
    def __init__(self, timestamp, leave_id, ):
        super().__init__(timestamp, TYPE = "CBTPNodeLeave", priority=0)
        self.leave_id = leave_id
    
    def process(self, sim):
        """处理离开事件"""
        print(f"[{sim.current_time}]节点{self.leave_id}离开")
        sim.signal += 1

        if sim.flag == False :
            sim.signal += 1
            new_event = CBTPNodeLeaveCompletedEvent(sim.current_time + Network.rewired_time, self.leave_id)
            sim.schedule(new_event)
            return
        elif sim.signal == 1:
            sim.flag = False
            sim.signal += 1
            new_event = CBTPNodeLeaveCompletedEvent(sim.current_time + Network.rewired_time, self.leave_id)
            sim.schedule(new_event)
        else:
            # 故障发生后只有一棵树可用，故带宽减半
            sim.signal += 1
            sim.current_bandwidth = sim.network.bandwidth / 2
            new_event = CBTPNodeLeaveCompletedEvent(sim.current_time + Network.rewired_time, self.leave_id)
            sim.schedule(new_event)


class CBTPNodeLeaveCompletedEvent(Event):
    def __init__(self, timestamp, leave_id):
        super().__init__(timestamp, TYPE="CBTPNodeLeaveCompleted", priority=0)
        self.leave_id = leave_id

    def process(self, sim):
        print(f"[{sim.current_time}]节点{self.leave_id}离开调整结束")
        sim.signal -= 1
        # 所有节点都调整完毕，恢复带宽
        if sim.signal == 0:
            sim.current_bandwidth = sim.network.bandwidth
            sim.flag = True
        sim.topology.erase_node(self.leave_id)

class CBTPNodeJoinEvent(Event):
    def __init__(self, timestamp, join_id, ):
        super().__init__(timestamp, TYPE="CBTPNodeJoin", priority=1)
        self.join_id = join_id
    
    def process(self, sim):
        if sim.flag == False:
            # 处在初始化阶段时，直接进行加入
            sim.signal += 1
            new_event = CBTPNodeJoinCompletedEvent(sim.current_time + Network.time_step, self.join_id)
            sim.schedule(new_event)
            return
        
        if sim.signal != 0 :
            # 树中有单个节点离开，或单个节点加入，推后加入
            new_event = CBTPNodeJoinEvent(sim.current_time + Network.time_step, self.join_id)
            sim.schedule(new_event)
            return
        
        print(f"[{sim.current_time}]节点{self.join_id}加入")  
        # 处理时间
        time = Network.rewired_time
        sim.current_bandwidth = sim.network.bandwidth / 2
        new_event = CBTPNodeJoinCompletedEvent(sim.current_time + time, self.join_id)
        sim.schedule(new_event)

class CBTPNodeJoinCompletedEvent(Event):
    def __init__(self, timestamp, join_id, ):
        super().__init__(timestamp, TYPE="CBTPNodeJoinCompleted",priority=1)
        self.join_id = join_id

    def process(self, sim):
        print(f"[{sim.current_time}]节点{self.join_id}加入调整结束")
        sim.signal -= 1
        # 所有节点都调整完毕，恢复带宽
        if sim.signal == 0:
            sim.current_bandwidth = sim.network.bandwidth
            sim.flag = True
        sim.topology.add_node(self.join_id)

if __name__ == '__main__':
    
    # 节点数
    size = 16
    # 生成初始事件
    leave_nodes = [
        (3, 1.0),
        (6, 2.3),
        (9, 3.1)
    ]

    topology = dbT_OPT(size)
    sim = SimulationKernel(topology=topology)
    sim.schedule(AllreduceEvent(start_time=0, data_size=1000))
    for leave_id, time in leave_nodes:
        sim.schedule(CBTPNodeLeaveEvent(timestamp=time, leave_id=leave_id))

    # 运行仿真
    sim.run()