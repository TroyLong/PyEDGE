########################
##        About       ##
########################
# This is a Barnes-Hut Tree. It might be used for neighborhood estimation if this makes it any faster.
# It also might be used to compare the closeness to estimations across multiple images
########################
## Imported Libraries ##
########################
from math import dist
import numpy as np
from anytree import NodeMixin, PreOrderIter
########################
## Internal Libraries ##
########################
from dataTypes.cell import CellNeighbor


Serial = 0
BodySerial = 0



# This is a rectangle object that also keeps up with its bisections
class Rectangle(object):
    def __init__(self,x,y,height,width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.midX = x + (width / 2)
        self.midY = y + (height / 2)
    # Checks if a given position falls inside the rectangle
    def is_position_inside(self,position):
        return (self.x <= position[0]) and (self.x+self.width > position[0])  \
            and (self.y <= position[1]) and (self.y+self.height > position[1])



#TODO:: Recomment this section to be clearer to the new purpose of this code
#This is the node to the Barnes-Hut tree structure. It was recycled from my n-body simulator.
class TreeNode(NodeMixin):
    def __init__(self,rect,cells=[],cutoff_threshold = 0,parent=None,children=None):
        # each node is serialized for easy naming scheme
        self.set_serial()
        #this the area under the control of the node
        self.rect = rect
        self.parent = parent
        #this is all of the cells in the node. The lowest node doesn
        self.cells = cells
        self.total_area = 0
        self.center_of_mass = [0,0]
        self.cutoff_threshold = cutoff_threshold
        #temp variable
        self.child_rects = []
        self.child_cell_partitions = [[],[],[],[]]
        if children:
            self.children = children
        if len(cells) > 0:
            self.__find_center_of_mass()
        if len(cells) > 1:
            self.__create_children_nodes()
        # Does this node have only 1 element?
        self.is_node_single_occupied = len(cells) == 1
    def set_serial(self):
        global Serial
        self.Serial = Serial
        Serial += 1


    # Functional Form
    # This should be more related to cellDist
    # Finds distances to neighbors and cell area for initial guess
    def build_neighbor_cell(self,cell):
        if(self.is_node_single_occupied):
            return CellNeighbor(self.cells[0],self._neighbor_cell_distance_to_border(cell))
            
    def _neighbor_cell_distance_to_border(self,cell):
        return cell.dist(self.cells[0])-cell.radius


    # Is cell far enough away to be considered seprate
    def is_internal_node_within_cutoff(self,cell):
        cellToNode = np.sqrt((cell.center[0]-self.center_of_mass[0])**2+(cell.center[1]-self.center_of_mass[1])**2)
        cellToNode = cellToNode if cellToNode != 0 else 0.000000001
        sd = self.rect.width/cellToNode
        return  sd >= self.cutoff_threshold

    def __find_center_of_mass(self):
        self.total_area = 0
        for cell in self.cells:
            self.center_of_mass[0] += cell.area*cell.center[0]
            self.center_of_mass[1] += cell.area*cell.center[1]
            self.total_area += cell.area
        if self.total_area == 0:
            self.total_area = 0.000000001
        self.center_of_mass[0] /= self.total_area
        self.center_of_mass[1] /= self.total_area

    def __create_children_nodes(self):
        self.__create_child_rectangles()
        self.__subdivide_cells()
        self.children = list()
        for i in range(4):
            TreeNode(self.child_rects[i],self.child_cell_partitions[i],self.cutoff_threshold).parent = self
    def __create_child_rectangles(self):
        height, width = self.rect.height/2, self.rect.width/2
        self.child_rects = [Rectangle(self.rect.x,self.rect.y,height,width),
                            Rectangle(self.rect.midX,self.rect.y,height,width),
                            Rectangle(self.rect.x,self.rect.midY,height,width),
                            Rectangle(self.rect.midX,self.rect.midY,height,width)]
    def __subdivide_cells(self):
        for cell in list(self.cells):
            for i in range(len(self.child_rects)):
                #which the cell in the childRect being checked
                if ((cell.center[0] >= self.child_rects[i].x)
                        and (cell.center[0] < (self.child_rects[i].x+self.child_rects[i].width))
                        and (cell.center[1] >= self.child_rects[i].y)
                        and (cell.center[1] < (self.child_rects[i].y+self.child_rects[i].height))):
                    self.child_cell_partitions[i].append(cell)
                    self.cells.remove(cell)