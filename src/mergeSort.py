from cell import cellTraits as ct


def findNeighbors(cell,deviation):
    deviation = deviation
    cell[ct.NEIGHBORGUESSES] = mergeSortNeighbors(cell[ct.NEIGHBORGUESSES])
    if len(cell[ct.NEIGHBORGUESSES]) > 0:
        maxDistance = cell[ct.NEIGHBORGUESSES][0][1]
        for possibleNeighbor in cell[ct.NEIGHBORGUESSES]:
            if (possibleNeighbor[1] < maxDistance+deviation):
                cell[ct.NEIGHBORS].append(possibleNeighbor[0])
            else:
                break
            maxDistance = possibleNeighbor[1]



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