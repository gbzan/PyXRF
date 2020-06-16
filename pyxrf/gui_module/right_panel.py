from PyQt5.QtWidgets import QTabWidget

from .wd_plots_preview import PreviewPlots
from .wd_plots_fitting_model import PlotFittingModel
from .wd_plots_xrf_maps import PlotXrfMaps
from .wd_plots_rgb_maps import PlotRgbMaps
from .useful_widgets import global_gui_variables


class RightPanel(QTabWidget):

    def __init__(self, *, gpc, gui_vars):
        super().__init__()

        # Global processing classes
        self.gpc = gpc
        # Global GUI variables (used for control of GUI state)
        self.gui_vars = gui_vars

        self.addTab(PreviewPlots(gpc=self.gpc, gui_vars=self.gui_vars), "Preview")
        self.addTab(PlotFittingModel(gpc=self.gpc, gui_vars=self.gui_vars), "Fitting Model")
        self.addTab(PlotXrfMaps(gpc=self.gpc, gui_vars=self.gui_vars), "XRF Maps")
        self.addTab(PlotRgbMaps(gpc=self.gpc, gui_vars=self.gui_vars), "RGB")

    def update_widget_state(self, condition=None):
        # TODO: this function has to enable tabs and widgets based on the current program state
        state_compute = global_gui_variables["gui_state"]["running_computations"]
        if state_compute:
            # Disable everything
            for i in range(self.count()):
                if i != self.currentIndex():
                    self.setTabEnabled(i, False)
                self.widget(i).setEnabled(False)
        else:
            state_file_loaded = self.gui_vars["gui_state"]["state_file_loaded"]
            state_model_exist = self.gui_vars["gui_state"]["state_model_exist"]
            state_xrf_map_exists = self.gui_vars["gui_state"]["state_xrf_map_exists"]

            if not state_file_loaded:
                self.setCurrentIndex(0)
            self.setTabEnabled(0, state_file_loaded)
            self.setTabEnabled(1, state_file_loaded & state_model_exist)
            self.setTabEnabled(2, state_xrf_map_exists)
            self.setTabEnabled(3, state_xrf_map_exists)

        # Propagate the call to 'update_widget_state' downstream
        for i in range(self.count()):
            self.widget(i).update_widget_state(condition)
