import gui.stateMachineFrame as sMF
from gui.controlPanels.statusPanel import StatusPanel
from gui.controlPanels.timeStatePanel import TimeStatePanel
from gui.controlPanels.zStatePanel import ZStatePanel
from gui.controlPanels.filterOptionsPanel import FilterOptionsPanel
from gui.controlPanels.neighborOptionsPanel import NeighborOptionsPanel
from gui.controlPanels.cellFocusPanel import CellFocusPanel
from gui.controlPanels.multiStateControl import KernelPanel
from gui.controlPanels.exportPanel import ExportPanel
from ..optionsFrame import OptionsZoneFrame

# This is the main Panel Window Section
class OptionsZoneFrame(OptionsZoneFrame):
    def __init__(self, master=None, state=None):
        super().__init__(master,state)
        self._create_status(0)
        self._create_time_state(0)
        self._create_z_state(1)
        self._create_filter(2)
        self._create_neighbor(3)
        self._create_kernel(4)
        self._create_export(4)

    def load(self,state):
        super().load(state)
        self.status.load(state)
        self.time_state.load(state)
        self.z_state.load(state)
        self.filter.load(state)
        self.neighbor.load(state)

    def save(self):
        # This insures default settings are saved to previous State if state is changed
        # This does NOT submit the changes for view
        if super().save():
            self.filter.save()
            self.neighbor.save()

    def update(self):
        self.status.update()
        self.time_state.update()
        self.z_state.update()
