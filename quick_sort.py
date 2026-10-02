# Name: Weevern Gong
# Project Title: MSCS532_Assignment4
# Description: This program implements quick sort for comparison with heap sort and merge sort.
# The last value in each portion is selected as the pivot.

# Quick sort explanation: Quick sort uses the last value as the pivot and divides the list around it.
# The smaller portion is sorted recursively, and the larger portion is sorted using a loop.
# This keeps stack space O(log n). Expected time is O(n log n) on random distinct values, with O(n^2) worst-case time.
# Sorted, reverse-sorted, and all-equal inputs can produce the worst case with this pivot rule.


def partition(arr, low, high):

    pivot = arr[high]
    boundary = low

    # Move values less than or equal to the pivot toward the left side
    for index in range(low, high):
        if arr[index] <= pivot:
            arr[boundary], arr[index] = arr[index], arr[boundary]
            boundary += 1

    arr[boundary], arr[high] = arr[high], arr[boundary]
    return boundary


def quick_sort_recursive(arr, low, high):

    while low < high:
        pivot_index = partition(arr, low, high)

        # Sort the smaller portion recursively to limit the recursion depth
        if pivot_index - low < high - pivot_index:
            quick_sort_recursive(arr, low, pivot_index - 1)
            low = pivot_index + 1
        else:
            quick_sort_recursive(arr, pivot_index + 1, high)
            high = pivot_index - 1


def quick_sort(arr):

    quick_sort_recursive(arr, 0, len(arr) - 1)
    return arr


def main():

    numbers_arr = [5, 2, 20, 9, 1, 5, 6, 3, 71, 8, 4, 56, 12]
    print("Input array:", numbers_arr)
    print("Array sorted in monotonically increasing order using Quick Sort:", quick_sort(numbers_arr))


if __name__ == "__main__":
    main()
