import sqlite3
from dataTypes.dataTypeTraits import cellTraits as cT
con = sqlite3.connect("Cell.db")
cur = con.cursor()

cur.execute('''CREATE TABLE cells
            (area, radius)''')

def loadCells(cells):
    tempCells = [(cell[cT.AREA],cell[cT.RADIUS]) for cell in cells]
    cur.executemany("INSERT INTO cells VALUES (?,?)", tempCells)
    con.commit()

# TODO:: I'm printing now, but I want to use a generating function in the future
def fetchall():
    cur.execute("SELECT * FROM cells")
    print(cur.fetchall())

def closeDatabase():
    con.close()