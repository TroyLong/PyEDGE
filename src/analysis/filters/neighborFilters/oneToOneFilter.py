#This checks for a one to one relationship between neighboring cells
#def oneToOneFilter(cells):
#    for cell in cells:
#        for neighbor in cell[cT.NEIGHBORS]:
#            oneToOne = False
#            for neighorsNeighbor in neighbor[cT.NEIGHBORS]:
#                if cell[cT.CENTER] == neighorsNeighbor[cT.CENTER]:
#                    oneToOne = True
#            if not oneToOne:
#                cell[cT.NEIGHBORS].remove(neighbor)