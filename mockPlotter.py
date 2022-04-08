from turtle import ycor
import matplotlib.pyplot as plt
import pandas as pd

df =  pd.read_csv("states.csv")

time_1 = df[df["Time"]==0]
time_2 = df[df["Time"]==1]
time_3 = df[df["Time"]==2]

x_cord_1 = time_1["X"].tolist()
y_cord_1 = time_1["Y"].tolist()
size1 = time_1["Area"].tolist()
x_cord_2 = time_2["X"].tolist()
y_cord_2 = time_2["Y"].tolist()
size2 = time_2["Area"].tolist()
x_cord_3 = time_3["X"].tolist()
y_cord_3 = time_3["Y"].tolist()
size3 = time_3["Area"].tolist()

plt.scatter(x_cord_1,y_cord_1,s=size1,edgecolors='black')
plt.scatter(x_cord_2,y_cord_2,s=size2,edgecolors='black')
plt.scatter(x_cord_3,y_cord_3,s=size3,edgecolors='black')

plt.show()