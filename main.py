import sys

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow
from database.schema import create_tables

# Cria o banco de dados e as tabelas, caso ainda não existam
create_tables()

app = QApplication(sys.argv)

janela = MainWindow()
janela.show()

sys.exit(app.exec())