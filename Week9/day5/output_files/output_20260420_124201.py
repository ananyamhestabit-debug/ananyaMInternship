"""
NEXUS AI - Generated Code
Task      : explain binary search and it's implementation.
Generated : 20260420_124201
"""

# --- Block 1 ---
# Binary Search Algorithm Implementation

def binary_search(arr, target):
    """
    Searches for a target element in a sorted array using binary search.

    Args:
        arr (list): A sorted list of elements.
        target: The target element to search for.

    Returns:
        int: The index of the target element if found, -1 otherwise.
    """
    # Initialize the low and high pointers to the start and end of the array
    low = 0
    high = len(arr) - 1

    while low <= high:
        # Calculate the middle index of the current search range
        mid = (low + high) // 2

        # Check if the target element is at the middle index
        if arr[mid] == target:
            return mid
        # If the target element is less than the middle element, search in the left half
        elif arr[mid] > target:
            high = mid - 1
        # If the target element is greater than the middle element, search in the right half
        else:
            low = mid + 1

    # If the target element is not found, return -1
    return -1


# Example usage:
arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target = 23

index = binary_search(arr, target)

if index != -1:
    print(f"Target element {target} found at index {index}.")
else:
    print(f"Target element {target} not found in the array.")