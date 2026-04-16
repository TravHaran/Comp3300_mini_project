import unittest

from models import Job
from schedulers.fifo_scheduler import FIFOScheduler
from schedulers.sjf_scheduler import SJFScheduler
from schedulers.priority_scheduler import PriorityScheduler
from schedulers.rr_scheduler import RRScheduler


class TestFIFOScheduler(unittest.TestCase):
    def test_fifo_basic(self):
        jobs = [
            Job("A", 0, 4, 2),
            Job("B", 1, 3, 1),
            Job("C", 2, 2, 3)
        ]

        result = FIFOScheduler(jobs).run()

        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [("A", 0, 4), ("B", 4, 7), ("C", 7, 9)]
        )

        self.assertEqual(result.turnaround, {
            "A": 4,
            "B": 6,
            "C": 7
        })

        self.assertEqual(result.waiting, {
            "A": 0,
            "B": 3,
            "C": 5
        })

        self.assertEqual(result.avg_turnaround, 17 / 3)
        self.assertEqual(result.avg_waiting, 8 / 3)

    def test_fifo_tie_break_by_pid(self):
        jobs = [
            Job("B", 0, 3, 1),
            Job("A", 0, 2, 2),
            Job("C", 0, 1, 3)
        ]

        result = FIFOScheduler(jobs).run()

        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [("A", 0, 2), ("B", 2, 5), ("C", 5, 6)]
        )

    def test_fifo_idle_cpu(self):
        jobs = [
            Job("A", 3, 2, 1),
            Job("B", 5, 1, 2)
        ]

        result = FIFOScheduler(jobs).run()

        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [("A", 3, 5), ("B", 5, 6)]
        )

        self.assertEqual(result.waiting["A"], 0)
        self.assertEqual(result.waiting["B"], 0)


class TestSJFScheduler(unittest.TestCase):
    def test_sjf_basic(self):
        jobs = [
            Job("A", 0, 6, 3),
            Job("B", 0, 2, 1),
            Job("C", 1, 3, 2)
        ]

        result = SJFScheduler(jobs).run()

        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [("B", 0, 2), ("C", 2, 5), ("A", 5, 11)]
        )

        self.assertEqual(result.turnaround, {
            "A": 11,
            "B": 2,
            "C": 4
        })

        self.assertEqual(result.waiting, {
            "A": 5,
            "B": 0,
            "C": 1
        })

    def test_sjf_tie_break_by_pid(self):
        jobs = [
            Job("B", 0, 3, 1),
            Job("A", 0, 3, 2),
            Job("C", 1, 1, 3)
        ]

        result = SJFScheduler(jobs).run()

        # At time 0, A and B are both ready with same burst, so A goes first
        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [("A", 0, 3), ("C", 3, 4), ("B", 4, 7)]
        )

    def test_sjf_non_preemptive_behavior(self):
        jobs = [
            Job("A", 0, 5, 1),
            Job("B", 1, 1, 2)
        ]

        result = SJFScheduler(jobs).run()

        # B arrives later but should not preempt A
        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [("A", 0, 5), ("B", 5, 6)]
        )


class TestPriorityScheduler(unittest.TestCase):
    def test_priority_basic(self):
        jobs = [
            Job("A", 0, 4, 3),
            Job("B", 0, 2, 1),
            Job("C", 0, 1, 2)
        ]

        result = PriorityScheduler(jobs).run()

        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [("B", 0, 2), ("C", 2, 3), ("A", 3, 7)]
        )

        self.assertEqual(result.turnaround, {
            "A": 7,
            "B": 2,
            "C": 3
        })

        self.assertEqual(result.waiting, {
            "A": 3,
            "B": 0,
            "C": 2
        })

    def test_priority_tie_break_by_pid(self):
        jobs = [
            Job("C", 0, 2, 1),
            Job("A", 0, 4, 1),
            Job("B", 0, 3, 1)
        ]

        result = PriorityScheduler(jobs).run()

        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [("A", 0, 4), ("B", 4, 7), ("C", 7, 9)]
        )

    def test_priority_non_preemptive_behavior(self):
        jobs = [
            Job("A", 0, 5, 3),
            Job("B", 1, 1, 1)
        ]

        result = PriorityScheduler(jobs).run()

        # B has higher priority but arrives after A starts, so no preemption
        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [("A", 0, 5), ("B", 5, 6)]
        )


class TestRRScheduler(unittest.TestCase):
    def test_rr_basic(self):
        jobs = [
            Job("A", 0, 6, 3),
            Job("B", 0, 2, 1),
            Job("C", 1, 3, 2)
        ]

        result = RRScheduler(jobs, quantum=2).run()

        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [
                ("A", 0, 2),
                ("B", 2, 4),
                ("C", 4, 6),
                ("A", 6, 8),
                ("C", 8, 9),
                ("A", 9, 11)
            ]
        )

        self.assertEqual(result.turnaround, {
            "A": 11,
            "B": 4,
            "C": 8
        })

        self.assertEqual(result.waiting, {
            "A": 5,
            "B": 2,
            "C": 5
        })

    def test_rr_quantum_larger_than_burst(self):
        jobs = [
            Job("A", 0, 2, 1),
            Job("B", 0, 1, 2)
        ]

        result = RRScheduler(jobs, quantum=10).run()

        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [("A", 0, 2), ("B", 2, 3)]
        )

    def test_rr_quantum_one(self):
        jobs = [
            Job("A", 0, 2, 1),
            Job("B", 0, 2, 2)
        ]

        result = RRScheduler(jobs, quantum=1).run()

        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [("A", 0, 1), ("B", 1, 2), ("A", 2, 3), ("B", 3, 4)]
        )

    def test_rr_idle_cpu(self):
        jobs = [
            Job("A", 3, 2, 1)
        ]

        result = RRScheduler(jobs, quantum=1).run()

        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [("A", 3, 4), ("A", 4, 5)]
        )

    def test_rr_jobs_arrive_during_execution(self):
        jobs = [
            Job("A", 0, 4, 1),
            Job("B", 1, 2, 2),
            Job("C", 2, 1, 3)
        ]

        result = RRScheduler(jobs, quantum=2).run()

        self.assertEqual(
            [(g.pid, g.start, g.end) for g in result.gantt],
            [("A", 0, 2), ("B", 2, 4), ("C", 4, 5), ("A", 5, 7)]
        )


class TestGeneralCases(unittest.TestCase):
    def test_single_job_all_algorithms(self):
        jobs = [Job("A", 0, 5, 1)]

        fifo_result = FIFOScheduler(jobs).run()
        sjf_result = SJFScheduler(jobs).run()
        priority_result = PriorityScheduler(jobs).run()
        rr_result = RRScheduler(jobs, quantum=2).run()

        self.assertEqual(fifo_result.turnaround["A"], 5)
        self.assertEqual(sjf_result.turnaround["A"], 5)
        self.assertEqual(priority_result.turnaround["A"], 5)
        self.assertEqual(rr_result.turnaround["A"], 5)

        self.assertEqual(fifo_result.waiting["A"], 0)
        self.assertEqual(sjf_result.waiting["A"], 0)
        self.assertEqual(priority_result.waiting["A"], 0)
        self.assertEqual(rr_result.waiting["A"], 0)


if __name__ == "__main__":
    unittest.main()