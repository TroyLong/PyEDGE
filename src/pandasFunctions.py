# This will probably be moved to related cell.py

import pandas
from dataTypes.dataTypeTraits import cellTraits as cT

# TODO:: Can I turn this into a generating function?
def cellToPandas(cell):
    return pandas.DataFrame([{
        "X":cell[cT.CENTER][0],
        "Y":cell[cT.CENTER][1],
        "Area":cell[cT.AREA],
        }])

def cellsToPandas(cells):
    dataFrame = pandas.DataFrame()
    for cell in cells:
        dataFrame = pandas.concat([dataFrame,cellToPandas(cell)],ignore_index=True)
    print(dataFrame)
    return dataFrame

