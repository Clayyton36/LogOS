import sys

from PySide6.QtWidgets import QApplication,QLabel

app = QApplication(sys.argv)

janela = QLabel("Bem-vindo ao LogOS")
janela.resize(400, 200)
janela.setWindowTitle("LogOS")
janela.show()

sys.exit(app.exec())