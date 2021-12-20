########################
##        About       ##
########################
# Mergesort algorithm cell neighbors by neighbor distance.
########################
## Internal Libraries ##
########################
from dataTypes.cell import cellTraits as ct

def mergeSortNeighbors(cells):
    if len(cells) <= 1:
        return cells
    half = len(cells)//2
    left = mergeSortNeighbors(cells[:half])
    right = mergeSortNeighbors(cells[half:])

    return merge(left,right)

def merge(left,right):
    temp = list()
    while (left and right):
        if left[0][1] < right[0][1]:
            temp.append(left[0])
            left = left[1:]
        else:
            temp.append(right[0])
            right = right[1:]
    if left:
        temp.extend(left)
    if right:
        temp.extend(right)
    return temp