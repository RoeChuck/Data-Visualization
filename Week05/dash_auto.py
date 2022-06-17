# Almost Increasing Sequence
# Given a sequence of integers as an array, determine whether it is possible to obtain a strictly increasing sequence by removing no more than one element from the array.

def almostIncreasingSequence(sequence):
    # Write your code here
    count = 0
    for i in range(len(sequence)):
        if sequence[i] <= sequence[i-1]:
            count += 1
            if count > 1:
                return False
            if i > 1 and sequence[i] <= sequence[i-2]:
                return False
    return True 