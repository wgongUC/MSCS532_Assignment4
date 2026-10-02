# Name: Weevern Gong
# Project Title: MSCS532_Assignment4
# Description: This program simulates one processor using a max-heap priority queue.
# It records task order, waiting time, turnaround time, and missed deadlines.

# Scheduler explanation: The scheduler adds all tasks that have arrived before selecting the next task.
# Run the highest-priority ready task to completion without interruption. Tasks arriving during
# execution wait until the processor is available. When no task is ready, jump to the next arrival.
# Deadlines are recorded for evaluation and do not change the scheduling order.
# For n tasks, sorting arrivals and processing the queue take expected O(n log n) time and O(n) space.


import csv
import json
from pathlib import Path

from priority_queue import PriorityQueue, Task


OUTPUT_DIRECTORY = Path(__file__).resolve().parent
RESULT_COLUMNS = [
    "Task ID", "Priority", "Arrival Time", "Duration", "Deadline", "Start Time",
    "Finish Time", "Waiting Time", "Turnaround Time", "Tardiness", "Missed Deadline",
]


def create_sample_tasks():

    return [
        Task("A", 3, 0, 4, 8),
        Task("B", 5, 0, 3, 5),
        Task("C", 4, 1, 2, 6),
        Task("D", 5, 2, 1, 4),
        Task("E", 1, 6, 2, 10),
        Task("F", 4, 6, 1, 9),
        Task("G", 2, 16, 2, 19),
    ]


def simulate_scheduler(tasks):

    tasks = list(tasks)
    if any(not isinstance(task, Task) for task in tasks):
        raise TypeError("The scheduler accepts Task objects.")
    if len({task.task_id for task in tasks}) != len(tasks):
        raise ValueError("Task IDs must be unique in a simulation.")

    # Sort by arrival time and keep the original order when arrival times are equal
    arrivals = sorted(tasks, key=lambda task: task.arrival_time)
    queue = PriorityQueue()
    next_arrival = 0
    current_time = 0
    results = []

    while next_arrival < len(arrivals) or not queue.is_empty():
        if queue.is_empty() and next_arrival < len(arrivals):
            current_time = max(current_time, arrivals[next_arrival].arrival_time)

        # Add all tasks that have arrived before selecting the next task
        while next_arrival < len(arrivals) and arrivals[next_arrival].arrival_time <= current_time:
            queue.insert(arrivals[next_arrival])
            next_arrival += 1

        task = queue.extract_max()
        start_time = current_time
        current_time += task.duration
        tardiness = max(0, current_time - task.deadline) if task.deadline is not None else 0

        results.append({
            "Task ID": task.task_id,
            "Priority": task.priority,
            "Arrival Time": task.arrival_time,
            "Duration": task.duration,
            "Deadline": task.deadline,
            "Start Time": start_time,
            "Finish Time": current_time,
            "Waiting Time": start_time - task.arrival_time,
            "Turnaround Time": current_time - task.arrival_time,
            "Tardiness": tardiness,
            "Missed Deadline": tardiness > 0,
        })

    return results


def summarize_results(results):

    count = len(results)
    elapsed_time = results[-1]["Finish Time"] if results else 0
    busy_time = sum(row["Duration"] for row in results)

    return {
        "task_count": count,
        "execution_order": [row["Task ID"] for row in results],
        "average_waiting_time": sum(row["Waiting Time"] for row in results) / count if count else 0,
        "average_turnaround_time": sum(row["Turnaround Time"] for row in results) / count if count else 0,
        "missed_deadlines": sum(row["Missed Deadline"] for row in results),
        "total_tardiness": sum(row["Tardiness"] for row in results),
        "elapsed_time": elapsed_time,
        "busy_time": busy_time,
        "idle_time": elapsed_time - busy_time,
        "utilization_percent": 100 * busy_time / elapsed_time if elapsed_time else 0,
    }


def main():

    results = simulate_scheduler(create_sample_tasks())
    summary = summarize_results(results)

    with (OUTPUT_DIRECTORY / "scheduler_results.csv").open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=RESULT_COLUMNS)
        writer.writeheader()
        writer.writerows(results)

    for row in results:
        print(f"Task {row['Task ID']}: {row['Start Time']} to {row['Finish Time']}, "
              f"wait {row['Waiting Time']}, missed deadline {row['Missed Deadline']}")
    print(json.dumps(summary, indent=2))
    print("Scheduler results saved to scheduler_results.csv")


if __name__ == "__main__":
    main()
