from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class RelatoriosPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titulo = QLabel("Relatorios")

        layout.addWidget(titulo)

        self.setLayout(layout)