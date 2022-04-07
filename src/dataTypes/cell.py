########################
## Imported Libraries ##
########################
from math import dist

class Cell(object):
    __slots__ = ("center","verticies","area","radius","neighbors")
    def __init__(self,center=None,verticies=None,area=0,radius=0,neighbors=None):
        self.center = center if center!=None else (0,0)
        self.verticies = verticies if verticies.all()!=None else ()
        self.area = area
        self.radius = radius
        self.neighbors = neighbors if neighbors!=None else ()

    def sortNeighbors(self):
        self.neighbors = sorted(self.neighbors, key=lambda neigh: neigh.distance_to_border)  

    def dist(self, cell):
        return dist(self.center,cell.center)
        
    def cleanNeighborList(self):
        cleaned = False
        for neighbor in self.neighbors:
            mutual = False
            for neighbors_neighbor in neighbor.cell.neighbors:
                mutual = self.cell == neighbors_neighbor.cell
            if not mutual:
                self.removeNeighbor(neighbor.cell)
                cleaned = True
        return cleaned

    def isCellNeighbor(self,cellNeighbor):
        return cellNeighbor in self.neighbors
    def removeNeighbor(self,neighbor):
        for neigh in self.neighbors:
            if neigh.cell == neighbor.cell:
                self.neighbors.remove(neighbor)

    def createAverageCell(self,cell):
        return Cell((self.center[0]+cell.center[0])/2,
                    (self.center[1]+cell.center[1])/2.
                    (self.area+cell.area)/2,
                    (self.radius+cell.radius)/2)
    def __eq__(self,cell):
        return self.center == cell.center


class CellNeighbor(object):
    __slots__ = ("cell","distance_to_border")
    def __init__(self,cell,distance_to_border=0):
        self.cell = cell
        self.distance_to_border = distance_to_border