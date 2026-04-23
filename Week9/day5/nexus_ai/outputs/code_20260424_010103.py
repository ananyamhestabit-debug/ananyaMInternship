# Quick Sort implementation in Python
def quick_sort(arr):
    # Base case: If the array has one or zero elements, it is already sorted
    if len(arr) <= 1:
        return arr
    else:
        # Select the first element as the pivot (can be any element for simplicity)
        pivot = arr[0]
        
        # Partition the array into two parts: elements less than the pivot and elements greater than the pivot
        # Use list comprehension for concise code
        # Comment: This is the critical part where the pivot selection can affect the algorithm's performance
        less_than_pivot = [x for x in arr[1:] if x <= pivot]  # Include pivot in this list by not using [1:]
        greater_than_pivot = [x for x in arr[1:] if x > pivot]

        # Recursively sort the two partitions and combine the results
        # Comment: This is where the divide-and-conquer approach is applied
        return quick_sort(less_than_pivot) + [pivot] + quick_sort(greater_than_pivot)

# Test the Quick Sort code
def print_result():
    arr = [64, 34, 25, 12, 22, 11, 90]
    arr = quick_sort(arr)
    print("Sorted array:", arr)

# Run the test
print_result()