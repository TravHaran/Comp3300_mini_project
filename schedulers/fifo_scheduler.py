from schedulers.base_scheduler import BaseScheduler
from models import GanttEntry


class FIFOScheduler(BaseScheduler):
    def run(self):
        # sort by arrival time, then lexicographically smallest pid
        jobs = sorted(self.jobs, key=lambda job: (job.arrival, job.pid))

        gantt = []
        time = 0

        for job in jobs:
            # if CPU is idle, jump to this job's arrival time
            start = max(time, job.arrival)
            end = start + job.burst

            gantt.append(GanttEntry(job.pid, start, end))

            time = end

        return self.build_result("FIFO", gantt)