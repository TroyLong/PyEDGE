########################
##        About       ##
########################
# These are a series of tests for neighbor finding.
# Split from neighborAnalysis.py because they are dealing with the data in completely different ways
# TODO:: RUN SPEED TESTS
########################
## Imported Libraries ##
########################
import copy
import dataTypes.cell as ce

#TODO:: Deepcopy might be too slow
#Functional Form, might require deepcopy to work properly though
def distance_filter(state,deviation):
    temp_cells = list(state.cells)
    for cell in temp_cells:
        cellular_distance_filter(cell,deviation)
    return tuple(temp_cells)

# Is not functional, since it removes from cell and cell neighbor
# If it is passed a copy, it is effectivily functional
def cellular_distance_filter(cell,deviation):
    cell.sort_neighbors()
    # this is the furthest distance to allowed neighbor. Starts at the shortest
    max_distance = cell.neighbors[0].distance_to_border if (len(cell.neighbors) > 0) else 0
    # Bypasses isWithinAllowedDistance() computation after it fails the first time
    past_allowed = False
    for possible_neighbor in list(cell.neighbors):
        # possibly faster to nest, but not as clean
        if (not past_allowed) and (is_within_allowed_distance(cell,possible_neighbor,max_distance,deviation)): 
            max_distance = possible_neighbor.distance_to_border
        else:
            past_allowed = True
        if past_allowed:
            cell.remove_neighbor(possible_neighbor)



#TODO:: This is messy, and both booleans are probably not neccessary
# checks if neighbor is within the limit on distances past the current max_distance
def is_within_allowed_distance(cell, possible_neighbor, max_distance,deviation):
    distLimit = 1.75*(cell.radius + possible_neighbor.cell.radius)
    neighbor_in_dist_limit = possible_neighbor.distance_to_border < distLimit
    neighbor_in_deviation_limit = possible_neighbor.distance_to_border < max_distance+deviation
    return neighbor_in_dist_limit and neighbor_in_deviation_limit