# Name: Weevern Gong
# Project Title: MSCS532_Assignment4
# Description: This program implements a task priority queue using a max-heap stored in a list.
# The queue supports insertion, extraction, priority increases, and checking whether it is empty.

# Priority queue explanation: Larger priority numbers are served first. Equal priorities are ordered
# by earlier arrival time, then insertion order. A dictionary maps each task ID to its heap index.
# Each exchange updates the task locations so a priority change does not require searching the entire list.
# Heap movement takes O(log n) time. Dictionary access is expected O(1), and list growth is amortized.
# The heap and index dictionary together use O(n) space.


from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Task:

    task_id: str
    priority: int
    arrival_time: int = 0
    duration: int = 1
    deadline: int | None = None

    def __post_init__(self):

        if not isinstance(self.task_id, str) or not self.task_id:
            raise ValueError("Task ID must be a nonempty string.")

        for value in (self.priority, self.arrival_time, self.duration):
            if type(value) is not int:
                raise TypeError("Priority, arrival time, and duration must be integers.")

        if self.arrival_time < 0 or self.duration <= 0:
            raise ValueError("Arrival time must be nonnegative and duration must be positive.")

        if self.deadline is not None:
            if type(self.deadline) is not int:
                raise TypeError("Deadline must be an integer or None.")
            if self.deadline < self.arrival_time:
                raise ValueError("Deadline cannot be earlier than arrival time.")


class PriorityQueue:

    def __init__(self):

        self._heap = []
        self._positions = {}
        self._next_sequence = 0

    def _rank(self, index):

        task, sequence = self._heap[index]
        return task.priority, -task.arrival_time, -sequence

    def _swap(self, first, second):

        self._heap[first], self._heap[second] = self._heap[second], self._heap[first]

        # Keep the task locations correct after each exchange
        self._positions[self._heap[first][0].task_id] = first
        self._positions[self._heap[second][0].task_id] = second

    def _sift_up(self, index):

        while index > 0:
            parent = (index - 1) // 2
            if self._rank(parent) >= self._rank(index):
                break
            self._swap(parent, index)
            index = parent

    def _sift_down(self, index):

        # Exchange with the child that should be served first until the heap property is restored
        while 2 * index + 1 < len(self._heap):
            child = 2 * index + 1
            right = child + 1
            if right < len(self._heap) and self._rank(right) > self._rank(child):
                child = right
            if self._rank(index) >= self._rank(child):
                break
            self._swap(index, child)
            index = child

    def insert(self, task):

        if not isinstance(task, Task):
            raise TypeError("The queue accepts Task objects.")
        if task.task_id in self._positions:
            raise ValueError("A task with this ID is already queued.")

        # Add the task as a leaf, then move it upward if its priority is higher
        index = len(self._heap)
        self._heap.append((task, self._next_sequence))
        self._next_sequence += 1
        self._positions[task.task_id] = index
        self._sift_up(index)

    def extract_max(self):

        if self.is_empty():
            raise IndexError("Cannot extract from an empty priority queue.")

        task = self._heap[0][0]
        last_entry = self._heap.pop()
        del self._positions[task.task_id]

        # Replace the root with the last entry and repair the remaining heap
        if self._heap:
            self._heap[0] = last_entry
            self._positions[last_entry[0].task_id] = 0
            self._sift_down(0)

        return task

    def increase_key(self, task_id, new_priority):

        if type(new_priority) is not int:
            raise TypeError("New priority must be an integer.")
        if task_id not in self._positions:
            raise KeyError("Task ID is not in the queue.")

        index = self._positions[task_id]
        task, sequence = self._heap[index]
        if new_priority < task.priority:
            raise ValueError("The new priority cannot be smaller than the current priority.")

        # Update the priority while keeping the task's original arrival time and insertion order
        self._heap[index] = (replace(task, priority=new_priority), sequence)
        self._sift_up(index)

    def is_empty(self):

        return len(self._heap) == 0


def main():

    queue = PriorityQueue()
    queue.insert(Task("A", 3))
    queue.insert(Task("B", 5))
    queue.insert(Task("C", 1))
    queue.increase_key("C", 6)

    print("Extraction order after increasing C from priority 1 to 6:")
    while not queue.is_empty():
        task = queue.extract_max()
        print(f"Task {task.task_id}: priority {task.priority}")
    print("Queue is empty:", queue.is_empty())


if __name__ == "__main__":
    main()
