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
import gui.mainFrame.mainFrame as applicationFrame
from app import AppCore

logging.basicConfig(level=logging.INFO,
                    handlers=[logging.FileHandler("debug.log",mode='a'),
                            logging.StreamHandler(sys.stdout)])

app = applicationFrame.MainFrame(appCore=AppCore())
app.master.title("PyEDGE")
app.mainloop()

logging.info("Exiting PyEDGE.")