from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titulo = QLabel("Dashboard")

        layout.addWidget(titulo)

        self.setLayout(layout)