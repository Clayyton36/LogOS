from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.ui.nova_devolucao_page import NovaDevolucaoPage

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("LogOS")
        self.resize(1000, 700)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout()

        # Título
        titulo = QLabel("LogOS")
        layout.addWidget(titulo)

        # Subtítulo
        subtitulo = QLabel("Sistema de Controle de Devoluções")
        layout.addWidget(subtitulo)

        # Botão
        botao = QPushButton("Nova Devolução")
        layout.addWidget(botao)

        central_widget.setLayout(layout)