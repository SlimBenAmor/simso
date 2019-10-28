"""
Rate Monotic algorithm for uniprocessor architectures.
"""
from simso.core import Scheduler
from simso.schedulers import scheduler

@scheduler("simso.schedulers.FP_mono_sub")
class FP_mono_sub(Scheduler):
    def init(self):
        self.ready_list = []

    def on_activate(self, job):
        self.ready_list.append(job)
        job.cpu.resched()

    def on_terminated(self, job):
        self.ready_list.remove(job)
        job.cpu.resched()

    def schedule(self, cpu):
        if self.ready_list:
            # job with the highest priority
            job = min(self.ready_list, key=lambda x: x.prio)
            min_priority = job.prio
            min_job_list = []
            for i in range(len(self.ready_list)):
                if self.ready_list[i].prio == min_priority:
                    min_job_list.append(self.ready_list[i])
            
            job = min(min_job_list, key=lambda x: x.sub_prio)
        else:
            job = None

        return (job, cpu)
