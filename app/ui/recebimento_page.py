from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class RecebimentoPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titulo = QLabel("Recebimento")

        layout.addWidget(titulo)

        self.setLayout(layout)