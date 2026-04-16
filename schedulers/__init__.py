from schedulers.fifo_scheduler import FIFOScheduler
from schedulers.sjf_scheduler import SJFScheduler
from schedulers.priority_scheduler import PriorityScheduler
from schedulers.rr_scheduler import RRScheduler


class SchedulerFactory:
    @staticmethod
    def create(policy, jobs, quantum=None):
        if policy == "FIFO":
            return FIFOScheduler(jobs)
        elif policy == "SJF":
            return SJFScheduler(jobs)
        elif policy == "PRIORITY":
            return PriorityScheduler(jobs)
        elif policy == "RR":
            if quantum is None:
                raise ValueError("Round Robin requires a quantum")
            return RRScheduler(jobs, quantum)
        else:
            raise ValueError("Unsupported policy")