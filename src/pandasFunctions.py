# This will probably be moved to related cell.py
import logging
import pandas

# TODO:: Can I turn this into a generating function?
def cellToPandas(cell,cellMeta):
    return pandas.DataFrame([{
        "Time":cellMeta[0],
        "ZLevel":cellMeta[1],
        "X":cell.center[0],
        "Y":cell.center[1],
        "Area":cell.area,
        "Radius":cell.radius
        }])

def cellsToPandas(cells,cellMeta):
    dataFrame = pandas.DataFrame()
    for cell in cells:
        dataFrame = pandas.concat([dataFrame,cellToPandas(cell,cellMeta)],ignore_index=True)
    return dataFrame

def statesToPandas(states):
    outputList = list()
    for z,zLevel in enumerate(states):
        for t,state in enumerate(zLevel):
            outputList.append(cellsToPandas(state.cells,(t,z)))
    return pandas.concat(outputList)