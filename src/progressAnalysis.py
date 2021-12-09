########################
##        About       ##
########################
# I'm always curious about the program length, and I hate counting by hand.
# I made it a MUCH better, and much shorter. It was one of the longer programs.
########################
## Imported Libraries ##
########################
# Graphing Libraries
import matplotlib.pyplot as plt
# System Libraries
import os
import sys
from datetime import datetime

date = datetime.now()
imageFileDate = date.strftime("%Y_%m_%d-%I:%M:%S_%p")
analysisDate = date.strftime("%m/%d%Y/ - (%I:%M:%S %p)")
pieChartFileName = str("/Code-Analysis/LinesPieChart"+imageFileDate+".png")
pieChartFileNameForPC = str(os.path.join(sys.path[0], str(".."+pieChartFileName)))
tableFileName = str(os.path.join(sys.path[0], str("../CODEANALYSIS.md")))

labels = 'Main File', 'Image Analysis', 'Neighbor Analysis', 'Multi-Neighbor Analysis', 'GUI', 'Progress Analysis'
filesBySection = list()
lineNumbersBySection = list()
totalLines = 0
commentLineNumbersBySection = list()
totalCommentLines = 0
percentCommentsToLinesBySection = list()

# Main File
filesBySection.append(['pyEDGE.py'])
# Image Analysis Files
filesBySection.append(['cell.py','segmentImage.py'])
# Neighbor Analysis Files
filesBySection.append(['mergeSort.py','neighborAnalysis.py','neighborFilters.py','tree.py','walkTree.py'])
# Multi-Neighbor Analysis Files
filesBySection.append(['imageState.py'])
# Gui Files
filesBySection.append(['gui.py','graphFrame.py','optionsFrame.py','controlPanel.py','topMenu.py'])
# Progress Analysis Files
filesBySection.append(['progressAnalysis.py'])

for section in filesBySection:
    lineNumbersBySection.append(0)
    commentLineNumbersBySection.append(0)
    for filename in section:
        with open(os.path.join(sys.path[0], filename)) as program:
            rawInputList = program.read().split('\n')
            lineNumbersBySection[-1] += len(rawInputList)
            if rawInputList[0].startswith("#"):
                commentLineNumbersBySection[-1] += 1
    totalLines += lineNumbersBySection[-1]
    totalCommentLines += commentLineNumbersBySection[-1]
    percentCommentsToLinesBySection.append(100*commentLineNumbersBySection[-1]/lineNumbersBySection[-1])



outputString = "\n## " + str(analysisDate) +"\n"
outputString += "![Code Sections by Percent of Total Lines](" + str(pieChartFileName) + ")\n\n"
outputString += "| Sections | Lines | Percent of Total | Comments | Percent of Total | Percent Comments to Lines in Section |\n"
outputString += "| ------- | ----- | ---------------- | -------- | ---------------- | ------------------------------------ |\n"
outputString += "| Total Code | {:d} | 100 | {:d} | {:.2f} | N/A |\n".format(totalLines,totalCommentLines,(100*totalCommentLines/totalLines))
for i in range(len(labels)):
    outputString += ("| {:s} | {:d} | {:.2f} | {:d} | {:.2f} | {:.2f} |\n".format(labels[i],lineNumbersBySection[i],(100*lineNumbersBySection[i]/totalLines),
                                                    commentLineNumbersBySection[i], (100*commentLineNumbersBySection[i]/totalCommentLines),
                                                    percentCommentsToLinesBySection[i]))

print(outputString)

figure, (ax1,ax2,ax3) = plt.subplots(1,3)
ax1.pie(lineNumbersBySection,startangle=90)
ax1.axis('equal')
ax1.set_title("Lines of Code by Section")
ax2.pie(commentLineNumbersBySection,startangle=90)
ax2.axis('equal')
ax2.set_title("Comments of Code by Section")
ax3.pie(percentCommentsToLinesBySection,startangle=90)
ax3.axis('equal')
ax3.set_title("Ratio of Comments to Total Lines by Section")
figure.set_size_inches(14.5, 5.5)
figure.legend(labels,loc="lower center")
plt.tight_layout()
figure.savefig(pieChartFileNameForPC, dpi=100)
plt.show()

with open(tableFileName, "a") as file:
    file.write(outputString)