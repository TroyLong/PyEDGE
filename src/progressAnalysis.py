########################
##        About       ##
########################
# I'm always curious about the program length, and I hate counting by hand.
# Could be better, but this is good enough for now
########################
## Imported Libraries ##
########################
# Graphing Libraries
import matplotlib.pyplot as plt
# System Libraries
import os
import sys

filePath = "src/"

imageAnalysisFiles = ['cell.py','segmentImage.py']
iA=0
for filename in imageAnalysisFiles:
    with open(os.path.join(sys.path[0], filename)) as program:
            rawInputList = program.read().split('\n')
            iA += len(rawInputList)

neighborAnalysisFiles = ['mergeSort.py','neighborAnalysis.py','neighborFilters.py','tree.py','walkTree.py']
nA = 0
for filename in neighborAnalysisFiles:
    with open(os.path.join(sys.path[0], filename)) as program:
            rawInputList = program.read().split('\n')
            nA += len(rawInputList)

multiImageAnalysisFiles = ['imageState.py']
mNA = 0
for filename in multiImageAnalysisFiles:
    with open(os.path.join(sys.path[0], filename)) as program:
            rawInputList = program.read().split('\n')
            mNA += len(rawInputList)

guiFiles = ['gui.py','graphFrame.py','optionsFrame.py','topMenu.py']
gF = 0
for filename in guiFiles:
    with open(os.path.join(sys.path[0], filename)) as program:
            rawInputList = program.read().split('\n')
            gF += len(rawInputList)

mainFile = ['pyEDGE.py']
mF = 0
for filename in mainFile:
    with open(os.path.join(sys.path[0], filename)) as program:
            rawInputList = program.read().split('\n')
            mF += len(rawInputList)

progressAnalysisFiles = ['progressAnalysis.py']
pA = 0
for filename in progressAnalysisFiles:
    with open(os.path.join(sys.path[0], filename)) as program:
            rawInputList = program.read().split('\n')
            pA += len(rawInputList)

print("Total Code                   : " + str(mF+iA+nA+mNA+gF+pA))
print("Main File Code               : " + str(mF))
print("Image Analysis Code          : " + str(iA))
print("Neighbor Analysis Code       : " + str(nA))
print("Multi Neighbor Analysis Code : " + str(mNA))
print("Gui Code                     : " + str(gF))
print("Progress Analysis Code       : " + str(pA))

graphLabels = 'Main File', 'Image Analysis', 'Neighbor Analysis', 'Multi Neighbor Analysis', 'Gui', 'Progress Analysis'
sizes = [mF,iA,nA,mNA,gF,pA]
figure, ax = plt.subplots()
ax.pie(sizes,labels=graphLabels,autopct='%1.1f%%')
ax.axis('equal')

plt.show()