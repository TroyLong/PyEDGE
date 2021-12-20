########################
##        About       ##
########################
# Mergesort algorithm cell neighbors by neighbor distance.
########################
## Internal Libraries ##
########################
from dataTypes.cell import cellTraits as ct
from dataTypes.cellNeighbor import cellNeighborTraits as cnt


def mergeSortNeighbors(neighborCells):
    if len(neighborCells) <= 1:
        return neighborCells
    half = len(neighborCells)//2
    left = mergeSortNeighbors(neighborCells[:half])
    right = mergeSortNeighbors(neighborCells[half:])

    return merge(left,right)

def merge(left,right):
    temp = list()
    while (left and right):
        if left[0][cnt.DISTANCE_TO_BORDER] < right[0][cnt.DISTANCE_TO_BORDER]:
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