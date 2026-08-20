from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
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
from app.ui.analise_page import AnalisePage
from app.ui.decisao_page import DecisaoPage
from app.ui.relatorios_page import RelatoriosPage
from app.ui.configuracoes_page import ConfiguracoesPage


def _criar_icone_logo():
    """Desenha o mesmo selo azul com "L" usado no Dashboard, em varias
    resolucoes, para servir de icone da janela/barra de tarefas."""
    icone = QIcon()
    for tamanho in (16, 32, 48, 64, 128):
        pixmap = QPixmap(tamanho, tamanho)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#2563eb"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, tamanho, tamanho)

        painter.setPen(QColor("#ffffff"))
        fonte = QFont("Segoe UI", int(tamanho * 0.55))
        fonte.setBold(True)
        painter.setFont(fonte)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "L")
        painter.end()

        icone.addPixmap(pixmap)

    return icone


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("LogOS")
        self.setWindowIcon(_criar_icone_logo())
        self.resize(1000, 700)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        layout_principal = QHBoxLayout()
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Páginas
        conteudo = QStackedWidget()
        paginas = {
            "Dashboard": DashboardPage(),
            "Nova Devolução": NovaDevolucaoPage(),
            "Consulta": ConsultaPage(),
            "Análise": AnalisePage(),
            "Decisão": DecisaoPage(),
            "Relatórios": RelatoriosPage(),
            "Configurações": ConfiguracoesPage(),
        }
        for pagina in paginas.values():
            conteudo.addWidget(pagina)

        # Menu lateral
        menu_widget = QWidget()
        menu_widget.setObjectName("menuLateral")
        menu_widget.setFixedWidth(220)

        menu = QVBoxLayout()
        menu.setContentsMargins(16, 16, 16, 16)
        menu.setSpacing(6)
        menu_widget.setLayout(menu)

        titulo = QLabel("LogOS")
        titulo.setObjectName("titulo")
        menu.addWidget(titulo)

        subtitulo = QLabel("Sistema de Controle de Devoluções")
        subtitulo.setObjectName("subtitulo")
        subtitulo.setWordWrap(True)
        menu.addWidget(subtitulo)

        menu.addSpacing(16)

        botoes_navegacao = []

        def navegar_para(nome, botao_clicado):
            pagina = paginas[nome]
            conteudo.setCurrentWidget(pagina)
            if hasattr(pagina, "ao_exibir"):
                pagina.ao_exibir()
            for botao in botoes_navegacao:
                botao.setChecked(botao is botao_clicado)

        for nome in paginas:
            botao = QPushButton(nome)
            botao.setObjectName("botaoNavegacao")
            botao.setCheckable(True)
            botao.setCursor(Qt.PointingHandCursor)
            botao.clicked.connect(lambda _checked, n=nome, b=botao: navegar_para(n, b))
            botoes_navegacao.append(botao)
            menu.addWidget(botao)

        botoes_navegacao[0].setChecked(True)
        conteudo.setCurrentWidget(next(iter(paginas.values())))

        botoes_por_nome = dict(zip(paginas.keys(), botoes_navegacao))

        def ir_para_analise(devolucao_id):
            navegar_para("Análise", botoes_por_nome["Análise"])
            paginas["Análise"].selecionar_devolucao(devolucao_id)

        def ir_para_decisao(devolucao_id):
            navegar_para("Decisão", botoes_por_nome["Decisão"])
            paginas["Decisão"].selecionar_devolucao(devolucao_id)

        paginas["Dashboard"].definir_navegacao(
            abrir_analise=ir_para_analise,
            abrir_decisao=ir_para_decisao,
        )

        menu.addStretch()

        layout_principal.addWidget(menu_widget)
        layout_principal.addWidget(conteudo)

        central_widget.setLayout(layout_principal)

        self.setStyleSheet("""
            * {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            #tituloPagina {
                font-size: 22px;
                font-weight: bold;
                color: #1f2937;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 6px 8px;
                color: #1f2937;
                background-color: #ffffff;
                selection-background-color: #2563eb;
                selection-color: #ffffff;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #2563eb;
            }
            #menuLateral {
                background-color: #1f2937;
            }
            #titulo {
                color: #ffffff;
                font-size: 20px;
                font-weight: bold;
            }
            #subtitulo {
                color: #9ca3af;
                font-size: 11px;
            }
            #botaoNavegacao {
                text-align: left;
                padding: 10px 12px;
                border: none;
                border-radius: 6px;
                color: #e5e7eb;
                background-color: transparent;
                font-size: 13px;
            }
            #botaoNavegacao:hover {
                background-color: #374151;
            }
            #botaoNavegacao:checked {
                background-color: #2563eb;
                color: #ffffff;
                font-weight: bold;
            }
        """)
