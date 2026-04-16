from schedulers.base_scheduler import BaseScheduler
from models import GanttEntry


class SJFScheduler(BaseScheduler):
    def run(self):
        time = 0
        completed = 0
        n = len(self.jobs)
        gantt = []
        done = set()

        while completed < n:
            ready = []

            for job in self.jobs:
                if job.arrival <= time and job.pid not in done:
                    ready.append(job)

            if not ready:
                time += 1
                continue

            # smallest burst, then lexicographically smallest pid
            ready.sort(key=lambda job: (job.burst, job.pid))
            current = ready[0]

            start = time
            end = time + current.burst

            gantt.append(GanttEntry(current.pid, start, end))

            time = end
            done.add(current.pid)
            completed += 1

        return self.build_result("SJF", gantt)