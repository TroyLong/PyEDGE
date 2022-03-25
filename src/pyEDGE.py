########################
##        About       ##
########################
# This is the startup file.
########################
## Internal Libraries ##
########################
# Gui Libraries
import logging
import sys
import gui.applicationFrame as applicationFrame
from app import AppCore

logging.basicConfig(level=logging.INFO,
                    handlers=[logging.FileHandler("debug.log",mode='a'),
                            logging.StreamHandler(sys.stdout)])

app = applicationFrame.AppFrame(appCore=AppCore())
app.master.title("PyEDGE")
app.mainloop()

logging.info("Exiting pyEDGE.")