"""
Partitionned EDF using PartitionedScheduler.
"""
from simso.core.Scheduler import SchedulerInfo
from simso.utils import PartitionedScheduler
from simso.schedulers import scheduler

@scheduler("simso.schedulers.P_FP")
class P_FP(PartitionedScheduler):
    def init(self):
        PartitionedScheduler.init(
            self, SchedulerInfo("simso.schedulers.FP_mono"))

    def packer(self):
        cpus = [[cpu, 0] for cpu in self.processors]

        for task in self.task_list:
            if (task._task_info.prio ==None):
                #First Fit
                m = cpus[0][1]
                j = 0
                # Find the processor with the lowest load.
                for i, c in enumerate(cpus):
                    if c[1] < m:
                        m = c[1]
                        j = i

                # Affect it to the task.
                self.affect_task_to_processor(task, cpus[j][0])

                # Update utilization.
                cpus[j][1] += float(task.wcet) / task.period
            else:
                # Affect it to the task.
                j = 0
                for i, c in enumerate(cpus):
                    if (c[0].identifier==task._task_info.cpu_map):
                        j = i
                        break
                
                self.affect_task_to_processor(task, cpus[j][0])
                # self.affect_task_to_processor(task, [cpu for cpu in self.processorsif cpu.identifier==task._task_info.cpu_map][0])

                # Update utilization.
                if (task._task_info.task_type !="DAG"):
                    cpus[j][1] += float(task.wcet) / task.period
        return True
