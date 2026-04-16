from collections import deque
from schedulers.base_scheduler import BaseScheduler
from models import GanttEntry


class RRScheduler(BaseScheduler):
    def __init__(self, jobs, quantum):
        super().__init__(jobs)
        self.quantum = quantum

    def run(self):
        sorted_jobs = sorted(self.jobs, key=lambda j: (j.arrival, j.pid))

        remaining = {job.pid: job.burst for job in sorted_jobs}
        gantt = []
        queue = deque()
        time = 0
        idx = 0

        while idx < len(sorted_jobs) and sorted_jobs[idx].arrival <= time:
            queue.append(sorted_jobs[idx])
            idx += 1

        while queue or idx < len(sorted_jobs):
            if not queue:
                time = sorted_jobs[idx].arrival
                while idx < len(sorted_jobs) and sorted_jobs[idx].arrival <= time:
                    queue.append(sorted_jobs[idx])
                    idx += 1

            current = queue.popleft()
            run_time = min(self.quantum, remaining[current.pid])

            start = time
            end = time + run_time
            time = end

            remaining[current.pid] -= run_time
            gantt.append(GanttEntry(current.pid, start, end))

            while idx < len(sorted_jobs) and sorted_jobs[idx].arrival <= time:
                queue.append(sorted_jobs[idx])
                idx += 1

            if remaining[current.pid] > 0:
                queue.append(current)

        return self.build_result("RR", gantt)