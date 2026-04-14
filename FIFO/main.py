import json
import sys


def fifo(jobs):
    jobs = sorted(jobs, key=lambda j: (j["arrival"], j["pid"]))

    gantt = []
    turnaround = {}
    waiting = {}
    time = 0

    for job in jobs:
        start = max(time, job["arrival"])
        end = start + job["burst"]

        gantt.append({
            "pid": job["pid"],
            "start": start,
            "end": end
        })

        turnaround[job["pid"]] = end - job["arrival"]
        waiting[job["pid"]] = turnaround[job["pid"]] - job["burst"]

        time = end

    avg_turnaround = round(sum(turnaround.values()) / len(jobs), 2)
    avg_waiting = round(sum(waiting.values()) / len(jobs), 2)

    metrics = {
        "turnaround": turnaround,
        "waiting": waiting,
        "avg_turnaround": avg_turnaround,
        "avg_waiting": avg_waiting
    }

    return gantt, metrics


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        data = json.load(f)

    jobs = data["jobs"]
    gantt, metrics = fifo(jobs)

    output = {
        "policy": "FIFO",
        "gantt": gantt,
        "metrics": metrics
    }

    print(json.dumps(output, indent=2))