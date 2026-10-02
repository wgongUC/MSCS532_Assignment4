# Name: Weevern Gong
# Project Title: MSCS532_Assignment4
# Description: This program implements merge sort for comparison with heap sort and quick sort.
# Two sorted halves are combined using one reusable temporary list.

# Merge sort explanation: Divide the current portion in half until each portion has at most one value.
# Merge the sorted halves by copying their smaller current values into temporary storage.
# Copy the combined portion back into the original list. The same storage is reused for every merge.
# Its best-case, average-case, and worst-case time complexities are Θ(n log n), with O(n) extra space.


def merge(arr, temp_arr, left, middle, right):

    left_index = left
    right_index = middle

    # Copy the smaller current value into temporary storage; right is the first index outside the portion
    for index in range(left, right):
        if right_index >= right or (left_index < middle and arr[left_index] <= arr[right_index]):
            temp_arr[index] = arr[left_index]
            left_index += 1
        else:
            temp_arr[index] = arr[right_index]
            right_index += 1

    for index in range(left, right):
        arr[index] = temp_arr[index]


def merge_sort_recursive(arr, temp_arr, left, right):

    if right - left <= 1:
        return

    middle = (left + right) // 2
    merge_sort_recursive(arr, temp_arr, left, middle)
    merge_sort_recursive(arr, temp_arr, middle, right)
    merge(arr, temp_arr, left, middle, right)


def merge_sort(arr):

    if len(arr) > 1:
        temp_arr = [0] * len(arr)
        merge_sort_recursive(arr, temp_arr, 0, len(arr))

    return arr


def main():

    numbers_arr = [5, 2, 20, 9, 1, 5, 6, 3, 71, 8, 4, 56, 12]
    print("Input array:", numbers_arr)
    print("Array sorted in monotonically increasing order using Merge Sort:", merge_sort(numbers_arr))


if __name__ == "__main__":
    main()
