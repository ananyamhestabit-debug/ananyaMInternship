# Report

**Task:** generate a python code for binary search

**Binary Search Code**

Binary search is an efficient algorithm for finding an item from a sorted list of items. It works by repeatedly dividing in half the portion of the list that could contain the item, until you've narrowed down the possible locations to just one.

Here's a Python implementation of binary search:

```python
def binary_search(arr, target):
    """
    Searches for the target element in the given sorted array.

    Args:
        arr (list): A sorted list of elements.
        target: The element to search for.

    Returns:
        int: The index of the target element if found, -1 otherwise.
    """
    # Initialize the low and high pointers
    low, high = 0, len(arr) - 1

    # Continue searching while the low pointer is less than or equal to the high pointer
    while low <= high:
        # Calculate the mid index
        mid = (low + high) // 2

        # If the target element is found at the mid index, return the mid index
        if arr[mid] == target:
            return mid
        # If the target element is less than the element at the mid index, update the high pointer
        elif arr[mid] > target:
            high = mid - 1
        # If the target element is greater than the element at the mid index, update the low pointer
        else:
            low = mid + 1

    # If the target element is not found, return -1
    return -1
```

**Example Use Cases:**

```python
# Create a sorted list of elements
arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

# Search for an element in the list
index = binary_search(arr, 23)
if index != -1:
    print(f"Element found at index {index}")
else:
    print("Element not found in the list")
```

This code implements the binary search algorithm to find an element in a sorted list. It uses a while loop to repeatedly divide the search space in half until the target element is found or the search space is empty. The time complexity of this algorithm is O(log n), where n is the number of elements in the list.

## Task
Generate a Python code for binary search.

## Steps Taken
1. Defined the function for binary search.
2. Declared the array and target value.
3. Implemented the binary search algorithm.
4. Handled edge cases (array is empty or target is not found).
5. Returned the result (index of target if found, -1 otherwise).
6. Tested the binary search function with sample inputs.

## Result
**Binary Search Code**

Binary search is an efficient algorithm for finding an item from a sorted list of items. It works by repeatedly dividing in half the portion of the list that could contain the item, until you've narrowed down the possible locations to just one.

Here's a Python implementation of binary search:

```python
def binary_search(arr, target):
    """
    Searches for the target element in the given sorted array.

    Args:
        arr (list): A sorted list of elements.
        target: The element to search for.

    Returns:
        int: The index of the target element if found, -1 otherwise.

    """
    # Check if the array is empty
    if not arr:
        return -1

    # Initialize the low and high pointers
    low = 0
    high = len(arr) - 1

    # Continue the search until the low pointer is less than or equal to the high pointer
    while low <= high:
        # Calculate the mid index
        mid = (low + high) // 2

        # Check if the target is found at the mid index
        if arr[mid] == target:
            return mid
        # If the target is less than the element at the mid index, update the high pointer
        elif arr[mid] > target:
            high = mid - 1
        # If the target is greater than the element at the mid index, update the low pointer
        else:
            low = mid + 1

    # If the target is not found, return -1
    return -1

# Test the binary search function with sample inputs
arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(binary_search(arr, 23))  # Output: 5
print(binary_search(arr, 10))  # Output: -1
print(binary_search([], 5))    # Output: -1

## Quality Score
9/10 (minor improvements can be made for handling edge cases and error handling)