from abc import ABC, abstractmethod
from models import GanttEntry, SchedulerResult


class BaseScheduler(ABC):
    def __init__(self, jobs):
        self.jobs = jobs

    @abstractmethod
    def run(self):
        pass

    def build_result(self, policy, gantt):
        finish_time = {}
        burst_of = {}
        arrival_of = {}

        for job in self.jobs:
            burst_of[job.pid] = job.burst
            arrival_of[job.pid] = job.arrival

        for entry in gantt:
            finish_time[entry.pid] = entry.end

        turnaround = {}
        waiting = {}

        for job in self.jobs:
            turnaround[job.pid] = finish_time[job.pid] - arrival_of[job.pid]
            waiting[job.pid] = turnaround[job.pid] - burst_of[job.pid]

        avg_turnaround = sum(turnaround.values()) / len(self.jobs)
        avg_waiting = sum(waiting.values()) / len(self.jobs)

        return SchedulerResult(
            policy=policy,
            gantt=gantt,
            turnaround=turnaround,
            waiting=waiting,
            avg_turnaround=avg_turnaround,
            avg_waiting=avg_waiting
        )