import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showMaximized()
    main_window.setWindowTitle('Spline Editor')


# Подключение стилей для главного окна
    with open('Spline_editr/dark.qss', 'r', encoding='utf-8') as style_sheet_file:
        main_window.setStyleSheet(style_sheet_file.read())
    sys.exit(app.exec())
