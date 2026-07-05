import sys

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow


app = QApplication(sys.argv)

janela = MainWindow()
janela.show()

sys.exit(app.exec())