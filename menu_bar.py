from PyQt5.QtWidgets import QAction, QMessageBox, QMenuBar


class MenuBar (QMenuBar):
    def __init__(self, main_window, spline_view, parent=None) -> None:
        super().__init__(parent)

        file_menu = self.addMenu('File')
        with open('Spline_editr/dark.qss', 'r', encoding='utf-8') as style_sheet_file:
            file_menu.setStyleSheet(style_sheet_file.read())

        open_action = file_menu.addAction('Open')
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(spline_view.show_dialog_open)

        save_action = file_menu.addAction('Save')
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(spline_view.show_dialog_save)

        close_action = file_menu.addAction('Close')
        close_action.setShortcut('Ctrl+X')
        close_action.triggered.connect(main_window.close)

        file_menu = self.addMenu('Edit')

        undo_action = QAction('Undo', self)
        file_menu.addAction(undo_action)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(spline_view.unde_spline_view)

        redo_action = QAction('Redo', self)
        file_menu.addAction(redo_action)
        redo_action.setShortcut('Shift+Z')
        redo_action.triggered.connect(spline_view.redo_spline_view)

        about_action = self.addAction('About')
        about_action.triggered.connect(self.about_window)

    def about_window(self):
        str_about = '''
Программа Spline Editor

Версия: 1.0
Ссылка: https://____'''
        msb_about = QMessageBox()
        with open('Spline_editr/dark.qss', 'r', encoding='utf-8') as style_sheet_file:
            msb_about.setStyleSheet(style_sheet_file.read())
        msb_about.setWindowTitle('About')
        msb_about.setText(str_about)
        msb_about.setStandardButtons(QMessageBox.Ok)
        msb_about.exec_()
