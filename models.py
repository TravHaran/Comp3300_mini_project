from dataclasses import dataclass


@dataclass
class Job:
    pid: str
    arrival: int
    burst: int
    priority: int = 0


@dataclass
class GanttEntry:
    pid: str
    start: int
    end: int


@dataclass
class SchedulerResult:
    policy: str
    gantt: list
    turnaround: dict
    waiting: dict
    avg_turnaround: float
    avg_waiting: float

    def to_dict(self):
        return {
            "policy": self.policy,
            "gantt": [
                {"pid": entry.pid, "start": entry.start, "end": entry.end}
                for entry in self.gantt
            ],
            "metrics": {
                "turnaround": self.turnaround,
                "waiting": self.waiting,
                "avg_turnaround": round(self.avg_turnaround, 2),
                "avg_waiting": round(self.avg_waiting, 2)
            }
        }