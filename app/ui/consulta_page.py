from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class ConsultaPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titulo = QLabel("Consulta")

        layout.addWidget(titulo)

        self.setLayout(layout)