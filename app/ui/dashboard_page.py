from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addStretch()

        logo = QHBoxLayout()
        logo.addStretch()

        selo = QLabel("L")
        selo.setFixedSize(64, 64)
        selo.setAlignment(Qt.AlignCenter)
        selo.setStyleSheet("""
            background-color: #2563eb;
            color: #ffffff;
            border-radius: 32px;
            font-size: 32px;
            font-weight: bold;
        """)
        logo.addWidget(selo)

        nome = QLabel("LogOS")
        nome.setStyleSheet("""
            font-size: 44px;
            font-weight: bold;
            color: #1f2937;
            margin-left: 16px;
        """)
        logo.addWidget(nome)

        logo.addStretch()
        layout.addLayout(logo)

        layout.addStretch()

        self.setLayout(layout)
