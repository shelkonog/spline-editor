from PyQt5.QtCore import QPointF, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSpinBox, QDoubleSpinBox, QComboBox
from knot import Knot

class ControlPanel(QWidget):
    state_changed = pyqtSignal(Knot)
    def __init__(self, width: int, height: int, parent=None):
        super().__init__(parent)

        self.state = Knot(QPointF(0,0))
        layout = QHBoxLayout()
        self.x_spinbox = QSpinBox()
        self.x_spinbox.setMaximum(width)
        self.x_spinbox.setPrefix('X = ')
        self.x_spinbox.valueChanged.connect(self.set_x)

        self.y_spinbox = QSpinBox()
        self.y_spinbox.setMaximum(height)
        self.y_spinbox.setPrefix('Y = ')
        self.y_spinbox.valueChanged.connect(self.set_y)

        self.combo = QComboBox()
        with open('Spline_editr/dark.qss', 'r', encoding='utf-8') as style_sheet_file:
            self.combo.setStyleSheet(style_sheet_file.read())
        data = ['Kochanek–Bartels', 'Polyline']
        self.combo.addItems(data)

        layout.addWidget(self.combo)
        layout.addWidget(self.x_spinbox)
        layout.addWidget(self.y_spinbox)

        def create_spinbox(prefix: str, min: float, max: float, slot) -> QDoubleSpinBox:
            spin = QDoubleSpinBox()
            spin.setPrefix(prefix)
            spin.setMinimum(min)
            spin.setMaximum(max)
            spin.valueChanged.connect(slot)
            layout.addWidget(spin)
            return spin

        self.t_spinbox = create_spinbox('T = ', -1000, 1000, self.set_tension)
        self.b_spinbox = create_spinbox('B = ', -1000, 1000, self.set_bias)
        self.c_spinbox = create_spinbox('C = ', -1000, 1000, self.set_continuity)
        self.setLayout(layout)

    def set_x(self, value: float):
        if value == self.state.pos.x():
            return
        self.state.pos.setX(value)
        self.state_changed.emit(self.state)

    def set_y(self, value: float):
        if value == self.state.pos.y():
            return
        self.state.pos.setY(value)
        self.state_changed.emit(self.state)

    def set_tension(self, value: float):
        if value == self.state.tension:
            return
        self.state.tension = value
        self.state_changed.emit(self.state)
    def set_bias(self, value: float):
        if value == self.state.bias:
            return
        self.state.bias = value
        self.state_changed.emit(self.state)
    def set_continuity(self, value: float):
        if value == self.state.continuity:
            return
        self.state.continuity = value
        self.state_changed.emit(self.state)

    def set_state(self, value: Knot):
        self.state = value
        self.x_spinbox.setValue(round(value.pos.x()))
        self.y_spinbox.setValue(round(value.pos.y()))
        self.t_spinbox.setValue(value.tension)
        self.b_spinbox.setValue(value.bias)
        self.c_spinbox.setValue(value.continuity)
