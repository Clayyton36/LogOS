from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QStackedWidget,
)

from app.ui.nova_devolucao_page import NovaDevolucaoPage

from app.ui.dashboard_page import DashboardPage
from app.ui.consulta_page import ConsultaPage
from app.ui.recebimento_page import RecebimentoPage
from app.ui.relatorios_page import RelatoriosPage
from app.ui.configuracoes_page import ConfiguracoesPage
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("LogOS")
        self.resize(1000, 700)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        
        layout_principal = QHBoxLayout()

        menu = QVBoxLayout()

        conteudo = QStackedWidget()
        dashboard = DashboardPage()
        nova_devolucao = NovaDevolucaoPage()
        consulta = ConsultaPage()
        recebimento = RecebimentoPage()
        relatorios = RelatoriosPage()
        configuracoes = ConfiguracoesPage()

        conteudo.addWidget(dashboard)
        conteudo.addWidget(consulta)
        conteudo.addWidget(recebimento)
        conteudo.addWidget(relatorios)
        conteudo.addWidget(configuracoes)

        conteudo.setCurrentWidget(dashboard)

        # Título
        titulo = QLabel("LogOS")
        menu.addWidget(titulo)

        # Subtítulo
        subtitulo = QLabel("Sistema de Controle de Devoluções")
        menu.addWidget(subtitulo)

        # Botão
        botao = QPushButton("Nova Devolução")
        menu.addWidget(botao)

        layout_principal.addLayout(menu)
        layout_principal.addWidget(conteudo)

        central_widget.setLayout(layout_principal)