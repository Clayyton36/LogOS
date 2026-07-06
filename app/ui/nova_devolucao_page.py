from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)


class NovaDevolucaoPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titulo = QLabel("Nova Devolução")
        layout.addWidget(titulo)

        self.setLayout(layout)