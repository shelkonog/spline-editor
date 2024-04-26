from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtGui import QPainter, QPalette, QPen, QBrush
from PyQt5.QtCore import Qt, pyqtSignal
from spline import Spline
from knot import Knot
from spline_history import SplineHistory
import pickle

class SplineView(QWidget):
    '''
    Класс вьюшка для рисования сплайнов
    '''
    # сигнал сигнал об изменении координат текущей точки сплайна
    current_knot_chaged = pyqtSignal(Knot)

    def __init__(self, parent=None):
        '''
        Устанавливает аттрибуты объекта:
        spline объект для описания сплайна
        spline_history объект для хранения истории рисования сплайна по точкам
        self.cur_knot_index индекс текущей точки сплайна
         self.type_spline способ рисования сплайна, два варианта ('Kochanek–Bartels', 'Polyline')
        '''
        super().__init__(parent)
        self.spline = Spline()
        self.spline_history = SplineHistory()
        self.spline_history.save_spline(self.spline.knots)
        self.cur_knot_index = None
        self.type_spline = 0

    def paintEvent(self, event):
        '''
        метод для рисования сплайна и точек
        '''
        bg_color = self.palette().color(QPalette.Base)
        curve_color = self.palette().color(QPalette.Foreground)
        painter = QPainter(self)
        painter.fillRect(self.rect(), bg_color)
        painter.setPen(QPen(curve_color, 2, Qt.SolidLine))
        painter.setRenderHints(QPainter.HighQualityAntialiasing)
        painter.setBrush(QBrush(curve_color, Qt.SolidPattern))

        # рисуем точки сплайна
        for index, knot in enumerate(self.spline.get_knots()):
            radius = 6 if self.cur_knot_index == index else 4
            painter.drawEllipse(knot.pos, radius, radius)

        # рисуем сплайн
        painter.drawPolyline(self.spline.get_curve(self.type_spline))
        return super().paintEvent(event)

    def mousePressEvent(self, event) -> None:
        '''
        Метод обработки нажатия клавиши мыши, для отрисовки и удаления точек
        левая клавиша, добавление точки или выделение существующей
        правая клаввиша удаление выбранной точки
        '''
        # инекс выбранной точки на splain_view
        index = self.spline.get_knot_by_pos(event.pos())

        button = event.button()

        # Обраьотка нажатия правой клавишей мыши на существующую точку сплайна
        if (button == Qt.RightButton) and (index is not None):
            self.cur_knot_index = index
        # удаляем выбранную точку
            self.spline.knots.pop(index)
        # обработка граничных значений для индекса текущей точки
            if self.cur_knot_index > len(self.spline.get_knots()) - 1:
                self.cur_knot_index = len(self.spline.get_knots()) - 1
            if len(self.spline.get_knots()) == 0:
                self.cur_knot_index = 0
        # сохранение текущего состояния сплайна
            self.spline_history.save_spline(self.spline.knots)
            self.spline.curve = None

        # Обраьотка нажатия левойклавишей мыши
        # Если выбрана существующая точка, то в метод paintEvent передадуться ее индекс
        # для прорисовки большим диаметром 6
        if button == Qt.LeftButton:
            if index is not None:
                self.cur_knot_index = index
        # иначе на spline_view будет добавлена новая точка
        # и сплайн нарисуется заново
            else:
                if len(self.spline.get_knots()) == 0:
                    self.cur_knot_index = 0
                else:
                    self.cur_knot_index += 1
                self.spline.add_knot(self.cur_knot_index, event.pos())
                self.spline_history.save_spline(self.spline.knots)
        # отправка сигнала об изменении координат текущей точки
        # для запуска обработчиков и корректировки значений спинбоксов
        if len(self.spline.get_knots()) > 0:
            self.current_knot_chaged.emit(self.spline.get_knots()[self.cur_knot_index])
        self.update()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        '''
        Метод обработки движения курсора при нажайто клавише мыши
        при этом перетаскивается точка и перерисовывается сплайн
        '''
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
