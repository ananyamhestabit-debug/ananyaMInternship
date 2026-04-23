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

# Create a sorted list of elements
arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

# Search for an element in the list
index = binary_search(arr, 23)
if index != -1:
    print(f"Element found at index {index}")
else:
    print("Element not found in the list")