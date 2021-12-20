########################
##        About       ##
########################
# This is the startup file.
########################
## Internal Libraries ##
########################
# Gui Libraries
import gui.applicationFrame as applicationFrame

app = applicationFrame.App()
app.master.title("PyEDGE")
app.mainloop()