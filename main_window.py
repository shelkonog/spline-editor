from PyQt5.QtWidgets import QMainWindow
from spline_view import SplineView
from control_panel import ControlPanel
from menu_bar import MenuBar


class MainWindow(QMainWindow):
    '''
    Класс главного окна
    '''
    def __init__(self, parent=None):
        '''
    Устанавливает аттрибуты объекта главное окно:
        spline_view     вьюшка для рисования сплайнов
        menubar         меню главного окна
        control_panel   контрольная панель
        '''
        super().__init__(parent)
        spline_view = SplineView()
        self.setCentralWidget(spline_view)

        menubar = MenuBar(self, spline_view)
        self.setMenuBar(menubar)

        control_panel = ControlPanel(spline_view.maximumWidth(), spline_view.maximumHeight())
        self.statusBar().addWidget(control_panel)
# state_changed  сигнал изменения значения спинбоксов на контрольной панели
# подключения обработчика set_current_knot при изменении спинбокса
        control_panel.state_changed.connect(spline_view.set_current_knot)

# подключения обработчика change_item_combo изменения значения комбобокса
        control_panel.combo.currentIndexChanged.connect(spline_view.change_item_combo)

# current_knot_chaged сигнал об изменении координат текущей точки сплайна
# подключения обработчика set_state
        spline_view.current_knot_chaged.connect(control_panel.set_state)
