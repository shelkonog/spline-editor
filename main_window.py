from PyQt5.QtWidgets import QMainWindow
from spline_view import SplineView
from control_panel import ControlPanel
from menu_bar import MenuBar

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        spline_view = SplineView()
        self.setCentralWidget(spline_view)

        menubar = MenuBar(self, spline_view)
        self.setMenuBar(menubar)

        control_panel = ControlPanel(spline_view.maximumWidth(), spline_view.maximumHeight())
        self.statusBar().addWidget(control_panel)

        control_panel.state_changed.connect(spline_view.set_current_knot)
        control_panel.combo.currentIndexChanged.connect(spline_view.change_item_combo)
        spline_view.current_knot_chaged.connect(control_panel.set_state)
