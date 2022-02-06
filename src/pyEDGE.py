########################
##        About       ##
########################
# This is the startup file.
########################
## Internal Libraries ##
########################
# Gui Libraries
import gui.applicationFrame as applicationFrame
from app import AppCore

app = applicationFrame.AppFrame(appCore=AppCore())
app.master.title("PyEDGE")
app.mainloop()