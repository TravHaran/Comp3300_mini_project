import json
import sys
from models import Job
from schedulers import SchedulerFactory


def load_input(filename):
    with open(filename, "r") as f:
        return json.load(f)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py input.json", file=sys.stderr)
        sys.exit(1)

    data = load_input(sys.argv[1])

    jobs = []
    for j in data["jobs"]:
        jobs.append(Job(
            pid=j["pid"],
            arrival=j["arrival"],
            burst=j["burst"],
            priority=j.get("priority", 0)
        ))

    policy = data["policy"]
    quantum = data.get("quantum")

    scheduler = SchedulerFactory.create(policy, jobs, quantum)
    result = scheduler.run()

    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()