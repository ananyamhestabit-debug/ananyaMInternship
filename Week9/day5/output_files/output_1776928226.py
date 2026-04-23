def bubble_sort(arr):
    """
    Sorts an array in ascending order using the bubble sort algorithm.
    
    Args:
    arr (list): The list of elements to be sorted.
    
    Returns:
    list: The sorted list.
    """
    
    # Get the length of the array
    n = len(arr)
    
    # Repeat the process until the array is sorted
    for i in range(n):
        
        # Initialize a flag to track if any swaps were made
        swapped = False
        
        # Iterate over the array from the first element to the (n-i-1)th element
        for j in range(n - i - 1):
            
            # If the current element is greater than the next element, swap them
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True  # Fix: swapped should be True, not Tru
        
        # If no swaps were made in the inner loop, the array is sorted
        if not swapped:
            break
    
    return arr

def bubble_sort(arr):
    """
    Sorts an array in ascending order using the bubble sort algorithm.
    
    Args:
    arr (list): The list of elements to be sorted.
    
    Returns:
    list: The sorted list.
    """
    
    # Get the length of the array
    n = len(arr)
    
    # Repeat the process until the array is sorted
    for i in range(n):
        
        # Initialize a flag to track if any swaps were made
        swapped = False
        
        # Iterate over the array from the first element to the (n-i-1)th element
        for j in range(n - i - 1):
            
            # If the current element is greater than the next element, swap them
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swaps were made in the current iteration, the array is sorted
        if not swapped:
            break
    
    return arr