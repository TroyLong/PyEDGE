# TODO:: THIS MIGHT NEED TO BELONG TO THE STATE OBJECT?


# Functional Form
# Removes cells to small to be real cells. Recreates cells to be tuple ready
# Currently doesn't protect against negative numbers
def remove_outlier_small_radii(state,deviations):
    cells = state.cells
    mean_radius = state.find_mean_cell_radii()
    deviation = state.cell_radius_deviation()
    temp_cells = list()
    for cell in cells:
        if cell.radius > (mean_radius - (deviations * deviation)):
            temp_cells.append(cell)
    return tuple(temp_cells)