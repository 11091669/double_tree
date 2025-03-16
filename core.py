import heapq

class Network:
    time_step = 0.1  # 时间步长
    rewired_time = 20  # 链路重连时长（时间步长的整数倍）
    bandwidth = 10e9  # 网络带宽设置为10GB
    latency = 0.01

class Event:
    def __init__(self, timestamp: float, TYPE="", priority=0):
        self.timestamp = timestamp  # 事件触发时间
        self.priority = priority    # 同时间事件优先级
        self.TYPE = TYPE
        
    def __lt__(self, other):
        """ heapq优先比较时间，其次优先级 """
        return (self.timestamp, self.priority) < (other.timestamp, other.priority)
        
    def process(self, sim):
        raise NotImplementedError

class EventQueue:
    def __init__(self):
        self._queue = []
        
    def push(self, event):
        heapq.heappush(self._queue, event)
        
    def pop(self):
        return heapq.heappop(self._queue)
        
    def is_empty(self):
        return len(self._queue) == 0
    
class SimulationKernel:
    def __init__(self, topology):
        self.event_queue = EventQueue()  # 事件队列
        self.current_time = 0.0
        self._stop_flag = False
        self.current_bandwidth = Network.bandwidth  # 当前带宽
        self.topology = topology  # 网络拓扑
        self.flag = True  # 状态码 True -> 正常  False -> 无法通信
        self.signal = 0  # 信号量
        self.stats = {
            'completed_times': [],
        }
        
    def schedule(self, event):
        """ 插入事件到队列 """
        if event.timestamp >= self.current_time:
            self.event_queue.push(event)
            
    def run(self):
        """ 推进仿真直到指定时间 """
        while not self.event_queue.is_empty() and not self._stop_flag:
            event = self.event_queue.pop()
            if self.flag == False and event.TYPE == "Allreduce":
                event.timestamp += Network.time_step
                self.event_queue.push(event)
                continue
            self.current_time = event.timestamp
            event.process(self)  # 处理事件
            
    def stop(self):
        self._stop_flag = True


class AllreduceEvent(Event):

    def __init__(self, start_time, data_size):
        super().__init__(start_time, TYPE = "Allreduce", priority = 2)
        self.data_size = data_size  # 剩余数据传输量
        
    def process(self, sim):
        """处理传输事件"""
        print(f"[{sim.current_time}]Allreduce剩余数据量为{self.data_size}")
        # 计算本次传输时间
        if self.data_size / sim.current_bandwidth < Network.time_step :
            # 数据量除以带宽小于时间步长，时间计算加上双向链路延迟
            time = Network.latency * sim.topology.height * 2 + self.data_size / sim.current_bandwidth
            transferred = self.data_size
        else:
            # 数据量大，采用流水线传输
            time = Network.time_step
            transferred = sim.current_bandwidth * time
        
        self.data_size -= transferred

        if self.data_size > 0:
            # 安排下一次传输
            new_event = AllreduceEvent(
                sim.current_time + time,
                self.data_size,
            )
            sim.schedule(new_event)
        else:
            sim.current_time += time
            print(f"[{sim.current_time}]传输完成")
            sim.stats['completed_times'].append(sim.current_time)
            