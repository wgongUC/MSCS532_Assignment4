# Name: Weevern Gong
# Project Title: MSCS532_Assignment4
# Description: This program compares heap sort, quick sort, and merge sort on several input arrangements.
# It saves median execution times, individual trials, and peak traced memory.

# Performance comparison explanation: Test 100, 500, 1000, and 2000 elements using random, sorted,
# reverse-sorted, repeated-value, and all-equal input. Each algorithm receives a copy of the same list.
# Check one warm-up run, then run five timed trials and record the median after verifying every result.
# Measure peak Python-traced memory separately so memory tracing does not affect execution times.
# Input copying, expected-result calculation, verification, and file output are outside the timer.


import csv
import random
import statistics
import time
import tracemalloc
from pathlib import Path

from heapsort import heap_sort
from merge_sort import merge_sort
from quick_sort import quick_sort


INPUT_SIZES = [100, 500, 1000, 2000]
NUMBER_OF_TRIALS = 5
RANDOM_SEED = 532
OUTPUT_DIRECTORY = Path(__file__).resolve().parent
ALGORITHMS = {"Heap Sort": heap_sort, "Quick Sort": quick_sort, "Merge Sort": merge_sort}


def create_datasets(size, random_generator):

    sorted_arr = list(range(size))
    random_arr = sorted_arr.copy()
    random_generator.shuffle(random_arr)

    return {
        "Random": random_arr,
        "Sorted": sorted_arr,
        "Reverse Sorted": list(reversed(sorted_arr)),
        "Repeated Values": [random_generator.randint(0, max(5, size // 20)) for i in range(size)],
        "All Equal": [7] * size,
    }


def verify_sorted_result(expected_arr, test_arr):

    if test_arr != expected_arr:
        raise ValueError("The sorting algorithm produced an incorrect result.")


def measure_execution_time(sort_function, input_arr):

    expected_arr = sorted(input_arr)
    warmup_arr = input_arr.copy()
    sort_function(warmup_arr)
    verify_sorted_result(expected_arr, warmup_arr)
    execution_times = []

    # Check each result before accepting its execution time
    for trial in range(NUMBER_OF_TRIALS):
        test_arr = input_arr.copy()
        start_time = time.perf_counter_ns()
        sort_function(test_arr)
        elapsed_ns = time.perf_counter_ns() - start_time
        verify_sorted_result(expected_arr, test_arr)
        execution_times.append(elapsed_ns / 1_000_000)

    return execution_times


def measure_peak_memory(sort_function, input_arr):

    expected_arr = sorted(input_arr)
    test_arr = input_arr.copy()
    tracemalloc.start()
    try:
        sort_function(test_arr)
        current_memory, peak_memory = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    verify_sorted_result(expected_arr, test_arr)
    return peak_memory / 1024


def run_performance_comparison():

    random_generator = random.Random(RANDOM_SEED)
    results = []
    trial_results = []

    for size in INPUT_SIZES:
        for dataset_name, input_arr in create_datasets(size, random_generator).items():
            for algorithm_name, sort_function in ALGORITHMS.items():
                times = measure_execution_time(sort_function, input_arr)
                peak_memory = measure_peak_memory(sort_function, input_arr)
                result = {"Algorithm": algorithm_name, "Dataset": dataset_name, "Input Size": size}
                results.append({
                    **result,
                    "Median Execution Time (ms)": statistics.median(times),
                    "Peak Traced Memory (KiB)": peak_memory,
                })
                for trial, elapsed_ms in enumerate(times, start=1):
                    trial_results.append({**result, "Trial": trial, "Execution Time (ms)": elapsed_ms})

    return results, trial_results


def save_csv(filename, rows):

    with (OUTPUT_DIRECTORY / filename).open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():

    results, trials = run_performance_comparison()
    save_csv("results.csv", results)
    save_csv("timing_trials.csv", trials)

    print(f"{'Algorithm':<12}{'Dataset':<18}{'Size':>6}{'Median (ms)':>16}{'Peak (KiB)':>14}")
    for row in results:
        print(f"{row['Algorithm']:<12}{row['Dataset']:<18}{row['Input Size']:>6}"
              f"{row['Median Execution Time (ms)']:>16.6f}{row['Peak Traced Memory (KiB)']:>14.3f}")
    print("Results saved to results.csv and timing_trials.csv")


if __name__ == "__main__":
    main()
