from FTCO import FTCO
from core import Network,Event,SimulationKernel,AllreduceEvent

class FTCONodeLeaveEvent(Event):
    def __init__(self, timestamp, leave_id):
        super().__init__(timestamp, TYPE = "FTCONodeLeave", priority=0)
        self.leave_id = leave_id
    
    def process(self, sim):
        """处理离开事件"""
        print(f"[{sim.current_time}]节点{self.leave_id}离开")
        sim.signal += 1
        sim.flag = False
        sim.current_bandwidth = 0

        new_event = FTCONodeLeaveCompletedEvent(sim.current_time + Network.rewired_time, self.leave_id)
        sim.schedule(new_event)

class FTCONodeLeaveCompletedEvent(Event):
    def __init__(self, timestamp, leave_id):
        super().__init__(timestamp, TYPE="FTCONodeLeaveCompleted", priority=0)
        self.leave_id = leave_id

    def process(self, sim):
        print(f"[{sim.current_time}]节点{self.leave_id}离开调整结束")
        sim.topology.erase_node(self.leave_id)
        sim.signal -= 1
        if sim.signal == 0:
            sim.current_bandwidth = sim.topology.bandwidth
            sim.flag = True
        