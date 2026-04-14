import json
import sys
from collections import deque

def load_input(filename):
    with open(filename, "r") as f:
        return json.load(f)

def round_robin(jobs, quantum):
    # Sort by arrival time, tie-break by lexicographically smallest PID
    sorted_jobs = sorted(jobs, key=lambda j: (j["arrival"], j["pid"]))

    remaining  = {j["pid"]: j["burst"]   for j in sorted_jobs}
    arrival_of = {j["pid"]: j["arrival"] for j in sorted_jobs}
    burst_of   = {j["pid"]: j["burst"]   for j in sorted_jobs}

    gantt = []
    queue = deque()
    time  = 0
    idx   = 0  # Pointer into sorted_jobs for next arrival

    # Seed queue with all jobs already available at t=0
    while idx < len(sorted_jobs) and sorted_jobs[idx]["arrival"] <= time:
        queue.append(sorted_jobs[idx]["pid"])
        idx += 1

    while queue or idx < len(sorted_jobs):
        # CPU idle: no ready process, jump clock to next arrival
        if not queue:
            time = sorted_jobs[idx]["arrival"]
            while idx < len(sorted_jobs) and sorted_jobs[idx]["arrival"] <= time:
                queue.append(sorted_jobs[idx]["pid"])
                idx += 1

        pid      = queue.popleft()
        run_time = min(quantum, remaining[pid])
        start    = time
        time    += run_time
        remaining[pid] -= run_time

        gantt.append({"pid": pid, "start": start, "end": time})

        # Enqueue jobs that arrived during this slice BEFORE re-adding
        # the current process, so they don't wait behind a job that just ran
        while idx < len(sorted_jobs) and sorted_jobs[idx]["arrival"] <= time:
            queue.append(sorted_jobs[idx]["pid"])
            idx += 1

        # Re-add current process if it still has burst remaining
        if remaining[pid] > 0:
            queue.append(pid)

    # Compute metrics
    finish_time = {}
    for seg in gantt:
        finish_time[seg["pid"]] = seg["end"]  # last write = actual finish

    turnaround = {pid: finish_time[pid] - arrival_of[pid] for pid in finish_time}
    waiting    = {pid: turnaround[pid]  - burst_of[pid]   for pid in turnaround}

    n = len(jobs)
    avg_turnaround = sum(turnaround.values()) / n
    avg_waiting    = sum(waiting.values())    / n

    return gantt, turnaround, waiting, avg_turnaround, avg_waiting

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py input.json", file=sys.stderr)
        sys.exit(1)

    data = load_input(sys.argv[1])
    policy = data.get("policy", "")
    jobs = data.get("jobs", [])

    if policy != "RR":
        print(json.dumps({"error": "This version only supports RR"}))
        sys.exit(0)

    # Ensure quantum is provided for Round Robin
    if "quantum" not in data:
        print(json.dumps({"error": "Round Robin requires a 'quantum' value in the JSON"}))
        sys.exit(0)

    quantum = data["quantum"]

    gantt, turnaround, waiting, avg_turnaround, avg_waiting = round_robin(jobs, quantum)

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