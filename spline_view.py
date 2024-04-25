from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QPainter, QPalette, QPen, QBrush
from PyQt5.QtCore import Qt, pyqtSignal
from spline import Spline
from knot import Knot
from spline_history import SplineHistory
import pickle

class SplineView(QWidget):
    current_knot_chaged = pyqtSignal(Knot)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.spline = Spline()
        self.spline_history = SplineHistory()
        self.spline_history.save_spline(self.spline.knots)
        self.cur_knot_index = None
        self.type_spline = 0

    def paintEvent(self, event):
        bg_color = self.palette().color(QPalette.Base)
        curve_color = self.palette().color(QPalette.Foreground)
        painter = QPainter(self)
        painter.fillRect(self.rect(), bg_color)
        painter.setPen(QPen(curve_color, 2, Qt.SolidLine))
        painter.setRenderHints(QPainter.HighQualityAntialiasing)
        painter.setBrush(QBrush(curve_color, Qt.SolidPattern))
        for index, knot in enumerate(self.spline.get_knots()):
            radius = 6 if self.cur_knot_index == index else 4
            painter.drawEllipse(knot.pos, radius, radius)

        painter.drawPolyline(self.spline.get_curve(self.type_spline))
        return super().paintEvent(event)

    def mousePressEvent(self, event) -> None:
        index = self.spline.get_knot_by_pos(event.pos())

        button = event.button()
        if (button == Qt.RightButton) and (index is not None):
            self.cur_knot_index = index
            self.spline.knots.pop(index)
            if self.cur_knot_index > len(self.spline.get_knots()) - 1:
                self.cur_knot_index = len(self.spline.get_knots()) - 1
            if len(self.spline.get_knots()) == 0:
                self.cur_knot_index = 0

            self.spline_history.save_spline(self.spline.knots)
            self.spline.curve = None

        if button == Qt.LeftButton:
            if index is not None:
                self.cur_knot_index = index
            else:
                if len(self.spline.get_knots()) == 0:
                    self.cur_knot_index = 0
                else:
                    self.cur_knot_index += 1
                self.spline.add_knot(self.cur_knot_index, event.pos())
                self.spline_history.save_spline(self.spline.knots)

        if len(self.spline.get_knots()) > 0:
            self.current_knot_chaged.emit(self.spline.get_knots()[self.cur_knot_index])
        self.update()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.spline.knots[self.cur_knot_index].pos = event.pos()
        self.current_knot_chaged.emit(self.spline.get_knots()[self.cur_knot_index])
        self.spline.curve = None
        self.update()
        return super().mouseMoveEvent(event)

    def set_current_knot(self, value: Knot):
        self.spline.set_current_knot(self.cur_knot_index, value)
        self.update()

    def unde_spline_view(self):
        if self.spline_history.cur_spline_index > 0:
            self.spline_history.cur_spline_index -= 1
        self.spline.knots = self.spline_history.copy_spline(self.spline_history.cur_spline_index)
        if len(self.spline.knots) > 0:
            self.cur_knot_index = len(self.spline.knots) - 1
            self.current_knot_chaged.emit(self.spline.knots[self.cur_knot_index])
        self.spline.curve = None
        self.update()

    def redo_spline_view(self):
        if self.spline_history.cur_spline_index < len(self.spline_history.list_splines) - 1:
            self.spline_history.cur_spline_index += 1
        self.spline.knots = self.spline_history.copy_spline(self.spline_history.cur_spline_index)

        if len(self.spline.knots) == 0:
            self.cur_knot_index = 0
        else:
            self.cur_knot_index = len(self.spline.knots) - 1
            self.current_knot_chaged.emit(self.spline.knots[self.cur_knot_index])

        self.spline.curve = None
        self.update()

    def show_dialog_save(self):
        fname = QFileDialog.getSaveFileName(self, 'Save file', '/home')[0]
        if fname == '':
            return
        else:
            with open(fname, 'wb') as file_name:
                pickle.dump(self.spline.knots, file_name)

    def show_dialog_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if fname == '':
            return
        else:
            with open(fname, 'rb') as file_name:
                self.spline.knots = pickle.load(file_name)
                self.spline.curve = None
                self.update()

    def change_item_combo(self, index):
        self.type_spline = index
        self.spline.curve = None
        self.update()
