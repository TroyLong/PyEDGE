########################
##        About       ##
########################
# This is the startup file.
########################
## Internal Libraries ##
########################
# Gui Libraries
import gui.applicationFrame as applicationFrame
from app import App

app = applicationFrame.AppFrame(appCore=App())
app.master.title("PyEDGE")
app.mainloop()