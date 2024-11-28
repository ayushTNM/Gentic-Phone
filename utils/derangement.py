# utils/derangement.py

import random


def derangement(lst):
    """
    Generates a derangement of the input list where no element remains in its original position.
    Returns None if a derangement is not possible.
    """
    n = len(lst)
    if n < 2:
        return None  # No derangement possible for n < 2

    attempts = 0
    max_attempts = 1000
    while attempts < max_attempts:
        shuffled = lst.copy()
        random.shuffle(shuffled)
        if all(shuffled[i] != lst[i] for i in range(n)):
            return shuffled
        attempts += 1
    return None  # Failed to find a derangement
