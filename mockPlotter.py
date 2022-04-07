from turtle import ycor
import matplotlib.pyplot as plt
import pandas as pd

df =  pd.read_csv("states.csv")

time1 = df[df["Time"]==0]
time2 = df[df["Time"]==1]
time3 = df[df["Time"]==2]

xCord1 = time1["X"].tolist()
yCord1 = time1["Y"].tolist()
size1 = time1["Area"].tolist()
xCord2 = time2["X"].tolist()
yCord2 = time2["Y"].tolist()
size2 = time2["Area"].tolist()
xCord3 = time3["X"].tolist()
yCord3 = time3["Y"].tolist()
size3 = time3["Area"].tolist()

plt.scatter(xCord1[::],yCord1[::],s=size1,edgecolors='black')
plt.scatter(xCord2,yCord2,s=size2,edgecolors='black')
plt.scatter(xCord3,yCord3,s=size3,edgecolors='black')

plt.show()