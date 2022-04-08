# This will probably be moved to related cell.py
import logging
import pandas

# TODO:: Can I turn this into a generating function?
def cell_to_pandas(cell,cell_meta):
    return pandas.DataFrame([{
        "Time":cell_meta[0],
        "ZLevel":cell_meta[1],
        "X":cell.center[0],
        "Y":cell.center[1],
        "Area":cell.area,
        "Radius":cell.radius
        }])

def cells_to_pandas(cells,cell_meta=None):
    cell_meta = cell_meta if cell_meta!=None else (0,0)
    df = pandas.DataFrame()
    for cell in cells:
        df = pandas.concat([df,cell_to_pandas(cell,cell_meta)],ignore_index=True)
    return df

def states_to_pandas(states):
    output = list()
    for z,z_level in enumerate(states):
        for t,state in enumerate(z_level):
            output.append(cells_to_pandas(state.cells,(t,z)))
    return pandas.concat(output)