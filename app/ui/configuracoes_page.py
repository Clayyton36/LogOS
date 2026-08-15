from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class ConfiguracoesPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)

        titulo = QLabel("Configurações")
        titulo.setObjectName("tituloPagina")

        layout.addWidget(titulo)

        self.setLayout(layout)