# CPU Scheduling Simulator

## Overview

This project implements a CPU scheduling simulator in Python. It
simulates classical scheduling algorithms and outputs both the execution
timeline (Gantt chart) and performance metrics in JSON format.

Supported algorithms: - FIFO (First-In First-Out) - SJF (Shortest Job
First, non-preemptive) - Priority (non-preemptive) - Round Robin (with
configurable quantum)

The simulator reads input from a JSON file and produces output strictly
in JSON format.

**Sample input/output json files for each algorithm can be found in the 'sample' folder**

------------------------------------------------------------------------

## How to Run

    python3 main.py input.json > output.json

-   `input.json` → contains scheduling policy and job definitions\
-   `output.json` → contains Gantt chart and computed metrics

------------------------------------------------------------------------

## Input Format

Example:

    {
      "policy": "RR",
      "quantum": 2,
      "jobs": [
        {"pid": "A", "arrival": 0, "burst": 6, "priority": 3},
        {"pid": "B", "arrival": 0, "burst": 2, "priority": 1},
        {"pid": "C", "arrival": 1, "burst": 3, "priority": 2}
      ]
    }

### Fields

-   `policy`: Scheduling algorithm (`FIFO`, `SJF`, `PRIORITY`, `RR`)
-   `quantum`: Required only for Round Robin
-   `jobs`: List of processes
    -   `pid`: Process ID (string)
    -   `arrival`: Arrival time
    -   `burst`: CPU burst time
    -   `priority`: Priority value (lower number = higher priority)

------------------------------------------------------------------------

## Output Format

Example:

    {
      "policy": "SJF",
      "gantt": [
        {"pid": "B", "start": 0, "end": 2},
        {"pid": "C", "start": 2, "end": 5},
        {"pid": "A", "start": 5, "end": 11}
      ],
      "metrics": {
        "turnaround": {"A": 11, "B": 2, "C": 4},
        "waiting": {"A": 5, "B": 0, "C": 1},
        "avg_turnaround": 5.67,
        "avg_waiting": 2.0
      }
    }

------------------------------------------------------------------------

## Project Structure

    project/
    │
    ├── main.py                # Entry point (handles JSON I/O)
    ├── models.py              # Data models (Job, GanttEntry, SchedulerResult)
    │
    ├── schedulers/            # Scheduling algorithm implementations
    │   ├── __init__.py        # SchedulerFactory
    │   ├── base_scheduler.py  # Shared logic (metrics computation)
    │   ├── fifo_scheduler.py
    │   ├── sjf_scheduler.py
    │   ├── priority_scheduler.py
    │   └── rr_scheduler.py
    │
    └── tests/
        └── test_schedulers.py # Unit tests for all algorithms

------------------------------------------------------------------------

## Design Overview

The project follows a simple object-oriented design based on the Factory pattern:

-   Each scheduling algorithm is implemented as its own class
-   All schedulers inherit from a common `BaseScheduler`
-   Shared logic (such as metric calculations) is centralized
-   A `SchedulerFactory` is used to instantiate the correct scheduler
-   Results are encapsulated in a `SchedulerResult` object

This keeps the design modular and maintainable.

------------------------------------------------------------------------

## Scheduling Rules

-   **Tie-breaking:** When multiple jobs are equally eligible, the
    lexicographically smallest PID is selected
-   **Non-preemptive algorithms (FIFO, SJF, Priority):** Once a job
    starts execution, it runs to completion
-   **Round Robin:**
    -   Uses a fixed time quantum
    -   Newly arrived jobs are added to the queue before re-adding the
        current job
-   **Idle CPU:** If no jobs are ready, time advances until the next job
    arrives

------------------------------------------------------------------------

## Metrics

-   **Turnaround Time** = completion time − arrival time
-   **Waiting Time** = turnaround time − burst time
-   Averages are computed across all jobs and rounded to 2 decimal
    places

------------------------------------------------------------------------

## Testing

Unit tests are implemented using Python's `unittest` framework.

### Run all tests:

    python3 -m unittest discover tests -v

### Test Coverage Includes:

-   Correct scheduling order for each algorithm
-   Metric correctness (turnaround and waiting times)
-   Tie-breaking rules
-   Non-preemptive behavior (SJF and Priority)
-   Round Robin behavior:
    -   different quantum sizes
    -   job arrivals during execution
-   CPU idle scenarios
-   Single-job cases

------------------------------------------------------------------------

## Assumptions

-   Time progresses in discrete integer units
-   Input JSON is well-formed
-   Process IDs (PIDs) are unique
-   Lower priority value indicates higher priority

------------------------------------------------------------------------

## Use of AI

AI tools were used to assist with brainstorming design ideas,
structuring the project, and identifying important edge cases for
testing. All implementation decisions and final code structure were
reviewed and refined manually.

------------------------------------------------------------------------

