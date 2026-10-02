# Name: Weevern Gong
# Project Title: MSCS532_Assignment4
# Description: This program checks the sorting algorithms, priority queue, and scheduler.
# The tests use simple inputs and expected results to check the assignment requirements.

# Testing explanation: Check each sorting algorithm and the max-heap property.
# Check task insertion, extraction, priority changes, and basic error handling.
# Verify the sample schedule and a few simple scheduler edge cases.


import unittest

from heapsort import build_max_heap, heap_sort
from merge_sort import merge_sort
from priority_queue import PriorityQueue, Task
from quick_sort import quick_sort
from scheduler_simulation import create_sample_tasks, simulate_scheduler, summarize_results


class SortingTests(unittest.TestCase):

    def test_heapsort_basic_correctness(self):

        # Check a representative list and a few simple edge cases
        for arr in [[5, 2, 20, 9, 1, 5, 6, 3], [], [5], [3, 1, 3, 1], [1, 2, 3, 4]]:
            with self.subTest(input_arr=arr):
                self.assertEqual(heap_sort(arr.copy()), sorted(arr))

    def test_quicksort_correctness(self):

        arr = [5, 2, 20, 9, 1, 5, 6, 3]
        self.assertEqual(quick_sort(arr.copy()), sorted(arr))

    def test_merge_sort_correctness(self):

        arr = [5, 2, 20, 9, 1, 5, 6, 3]
        self.assertEqual(merge_sort(arr.copy()), sorted(arr))

    def test_max_heap_construction(self):

        arr = [5, 3, 17, 10, 84, 19, 6, 22, 9]
        expected = sorted(arr)
        build_max_heap(arr)
        self.assertEqual(sorted(arr), expected)

        # Each parent must be at least as large as its child
        for index in range(1, len(arr)):
            self.assertGreaterEqual(arr[(index - 1) // 2], arr[index])


class PriorityQueueTests(unittest.TestCase):

    def test_priority_queue_insert_extract(self):

        queue = PriorityQueue()
        for task in [Task("A", 3), Task("B", 5), Task("C", 1)]:
            queue.insert(task)
        self.assertFalse(queue.is_empty())
        self.assertEqual([queue.extract_max().task_id for i in range(3)], ["B", "A", "C"])
        self.assertTrue(queue.is_empty())

    def test_priority_queue_increase_key(self):

        queue = PriorityQueue()
        for task in [Task("A", 3), Task("B", 5), Task("C", 1)]:
            queue.insert(task)
        queue.increase_key("C", 6)
        self.assertEqual([queue.extract_max().task_id for i in range(3)], ["C", "B", "A"])

    def test_priority_queue_basic_error_handling(self):

        queue = PriorityQueue()
        with self.assertRaises(IndexError):
            queue.extract_max()
        queue.insert(Task("A", 2))
        with self.assertRaises(ValueError):
            queue.increase_key("A", 1)
        with self.assertRaises(KeyError):
            queue.increase_key("missing", 4)


class SchedulerTests(unittest.TestCase):

    def test_scheduler_sample_scenario(self):

        results = simulate_scheduler(create_sample_tasks())
        self.assertEqual([row["Task ID"] for row in results], ["B", "D", "C", "F", "A", "E", "G"])
        summary = summarize_results(results)
        self.assertEqual(summary["task_count"], 7)
        self.assertAlmostEqual(summary["average_waiting_time"], 16 / 7)
        self.assertAlmostEqual(summary["average_turnaround_time"], 31 / 7)
        self.assertEqual(summary["missed_deadlines"], 2)
        self.assertEqual(summary["total_tardiness"], 6)
        self.assertEqual(summary["idle_time"], 3)
        self.assertAlmostEqual(summary["utilization_percent"], 100 * 15 / 18)

    def test_scheduler_basic_edge_cases(self):

        # Check an idle gap between tasks and an empty workload
        results = simulate_scheduler([Task("A", 1, 0, 1), Task("B", 2, 4, 1)])
        self.assertEqual([row["Start Time"] for row in results], [0, 4])
        self.assertEqual(summarize_results(results)["idle_time"], 3)
        self.assertEqual(simulate_scheduler([]), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
