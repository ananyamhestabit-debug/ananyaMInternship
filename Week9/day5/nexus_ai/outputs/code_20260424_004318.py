def merge_sort(arr):
    """
    Sorts an array using the merge sort algorithm.

    Args:
    arr (list): The list of elements to be sorted.

    Returns:
    list: The sorted list.
    """
    # Base case: If the array has one or zero elements, it is already sorted
    if len(arr) <= 1:
        return arr
    
    # Calculate the middle index to split the array into two halves
    mid = len(arr) // 2
    
    # Split the array into two halves
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    # Recursively sort the two halves
    left_half = merge_sort(left_half)  # Sort the left half
    right_half = merge_sort(right_half)  # Sort the right half
    
    # Merge the two sorted halves
    return merge(left_half, right_half)


def merge(left, right):
    """
    Merges two sorted lists into a single sorted list.

    Args:
    left (list): The first sorted list.
    right (list): The second sorted list.

    Returns:
    list: The merged sorted list.
    """
    # Initialize an empty list to store the merged result
    merged = []
    
    # Initialize indices to track the current position in both lists
    left_index = 0
    right_index = 0
    
    # Merge smaller elements first
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:  # If the current element in the left list is smaller
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])  # Otherwise, append the current element from the right list
            right_index += 1
    
    # Append any remaining elements from the left or right lists
    merged.extend(left[left_index:])  # Append the remaining elements from the left list
    merged.extend(right[right_index:])  # Append the remaining elements from the right list
    
    return merged


# Example usage:
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = merge_sort(numbers)
print("Sorted numbers:", sorted_numbers)