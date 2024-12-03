# utils/derangement.py

def derangement(lst):
    """
    Generates a derangement of the input list by shifting elements by one position.
    Returns None if a derangement is not possible.
    
    Parameters:
        lst (list): The input list to derange.
    
    Returns:
        list or None: The deranged list or None if derangement isn't possible.
    """
    n = len(lst)
    if n < 2:
        return None  # No derangement possible for lists with fewer than 2 elements

    # Shift the list by one position to the left
    deranged = lst[1:] + lst[:1]
    return deranged
