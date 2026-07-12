from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class ConfiguracoesPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titulo = QLabel("Configurações")

        self.setLayout(layout)