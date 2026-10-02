# Name: Weevern Gong
# Project Title: MSCS532_Assignment4
# Description: This program implements heap sort using a max-heap stored in a list.
# The largest value is moved to the end of the remaining heap until the list is sorted.

# Heap sort explanation: Heap sort first builds a max-heap from the input list.
# The largest value is moved to the end, and the remaining heap is repaired.
# These steps repeat until the list is sorted. Using a loop for heap repair keeps extra space constant.
# Building the heap takes O(n) time, and the complete sort has an O(n log n) upper bound for
# the best, average, and worst cases.


def max_heapify(arr, heap_size, root):

    # Move the root downward until it is at least as large as both children
    while 2 * root + 1 < heap_size:
        left = 2 * root + 1
        right = left + 1
        largest = root

        if arr[left] > arr[largest]:
            largest = left
        if right < heap_size and arr[right] > arr[largest]:
            largest = right

        if largest == root:
            break

        arr[root], arr[largest] = arr[largest], arr[root]
        root = largest


def build_max_heap(arr):

    # Leaves are already heaps, so begin at the last internal node
    for root in range(len(arr) // 2 - 1, -1, -1):
        max_heapify(arr, len(arr), root)

    return arr


def heap_sort(arr):

    build_max_heap(arr)

    # Place the largest remaining value into its final sorted position
    for end in range(len(arr) - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        max_heapify(arr, end, 0)

    return arr


def main():

    numbers_arr = [5, 2, 20, 9, 1, 5, 6, 3, 71, 8, 4, 56, 12]
    print("Input array:", numbers_arr)
    print("Array sorted in monotonically increasing order using Heap Sort:", heap_sort(numbers_arr))


if __name__ == "__main__":
    main()
