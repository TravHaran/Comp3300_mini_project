import json
import sys

def load_input(filename):
    with open(filename, "r") as f:
        return json.load(f)

def priority_non_preemptive(jobs):
    time = 0
    completed = 0
    n = len(jobs)
    gantt = []
    turnaround = {}
    waiting = {}
    done = set()

    while completed < n:
        ready = []
        for job in jobs:
            if job["arrival"] <= time and job["pid"] not in done:
                ready.append(job)

        if not ready:
            time += 1
            continue

        # Priority: pick lowest priority number (highest priority)
        # Tie-breaker: lexicographically smallest PID
        ready.sort(key=lambda job: (job["priority"], job["pid"]))
        current = ready[0]

        start_time = time
        end_time = time + current["burst"]

        gantt.append({
            "pid": current["pid"],
            "start": start_time,
            "end": end_time
        })

        time = end_time

        ta = end_time - current["arrival"]
        wt = ta - current["burst"]
        turnaround[current["pid"]] = ta
        waiting[current["pid"]] = wt
        done.add(current["pid"])
        completed += 1

    avg_turnaround = sum(turnaround.values()) / n
    avg_waiting = sum(waiting.values()) / n

    return gantt, turnaround, waiting, avg_turnaround, avg_waiting

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py input.json", file=sys.stderr)
        sys.exit(1)

    data = load_input(sys.argv[1])
    policy = data["policy"]
    jobs = data["jobs"]

    if policy != "PRIORITY":
        print(json.dumps({"error": "This version only supports PRIORITY"}))
        sys.exit(0)

    gantt, turnaround, waiting, avg_turnaround, avg_waiting = priority_non_preemptive(jobs)

    output = {
        "policy": policy,
        "gantt": gantt,
        "metrics": {
            "turnaround": turnaround,
            "waiting": waiting,
            "avg_turnaround": round(avg_turnaround, 2),
            "avg_waiting": round(avg_waiting, 2)
        }
    }

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()