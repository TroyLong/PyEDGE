from turtle import ycor
import matplotlib.pyplot as plt
import pandas as pd

df =  pd.read_csv("states.csv")

z_level_1 = df[df["ZLevel"]==0]
z_level_2 = df[df["ZLevel"]==1]
z_level_3 = df[df["ZLevel"]==2]

hi = -1
low = 0

x_cord_1 = z_level_1["X"].tolist()[low:hi]
y_cord_1 = z_level_1["Y"].tolist()[low:hi]
size1 = z_level_1["Area"].tolist()[low:hi]
x_cord_2 = z_level_2["X"].tolist()[low:hi]
y_cord_2 = z_level_2["Y"].tolist()[low:hi]
size2 = z_level_2["Area"].tolist()[low:hi]
x_cord_3 = z_level_3["X"].tolist()[low:hi]
y_cord_3 = z_level_3["Y"].tolist()[low:hi]
size3 = z_level_3["Area"].tolist()[low:hi]

print(f"{len(x_cord_1)}, {len(x_cord_2)}, {len(x_cord_3)}")

plt.scatter(x_cord_1,y_cord_1,s=size1,edgecolors='black')
plt.scatter(x_cord_2,y_cord_2,s=size2,edgecolors='black')
plt.scatter(x_cord_3,y_cord_3,s=size3,edgecolors='black')

plt.show()