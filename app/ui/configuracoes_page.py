from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
    QMessageBox,
)

from app.controllers.configuracoes_controller import ConfiguracoesController, ConfiguracaoValidationError


class ConfiguracoesPage(QWidget):

    def __init__(self, controller: ConfiguracoesController = None):
        super().__init__()

        self.controller = controller or ConfiguracoesController()

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)

        titulo = QLabel("Configurações")
        titulo.setObjectName("tituloPagina")
        layout.addWidget(titulo)

        subtitulo = QLabel("Condições do produto")
        subtitulo.setStyleSheet("font-size: 15px; font-weight: bold; color: #1f2937; margin-top: 12px;")
        layout.addWidget(subtitulo)

        explicacao = QLabel("Opções disponíveis no campo \"Condição do produto\" da página de Análise.")
        explicacao.setStyleSheet("color: #6b7280; font-size: 12px;")
        layout.addWidget(explicacao)

        self.lista_condicoes = QListWidget()
        layout.addWidget(self.lista_condicoes)

        adicionar = QHBoxLayout()

        self.campo_nova_condicao = QLineEdit()
        self.campo_nova_condicao.setPlaceholderText("Nova condição do produto")
        self.campo_nova_condicao.returnPressed.connect(self.adicionar_condicao)
        adicionar.addWidget(self.campo_nova_condicao)

        botao_adicionar = QPushButton("Adicionar")
        botao_adicionar.clicked.connect(self.adicionar_condicao)
        adicionar.addWidget(botao_adicionar)

        layout.addLayout(adicionar)

        botao_remover = QPushButton("Remover selecionada")
        botao_remover.clicked.connect(self.remover_condicao)
        layout.addWidget(botao_remover)

        layout.addStretch()

        self.setLayout(layout)

        self.ao_exibir()

    def ao_exibir(self):
        self._recarregar_lista()

    def _recarregar_lista(self):
        self.lista_condicoes.clear()
        for condicao in self.controller.listar_condicoes_produto():
            self.lista_condicoes.addItem(condicao["nome"])
            self.lista_condicoes.item(self.lista_condicoes.count() - 1).setData(Qt.UserRole, condicao["id"])

    def adicionar_condicao(self):
        try:
            self.controller.adicionar_condicao_produto(self.campo_nova_condicao.text())
        except ConfiguracaoValidationError as erro:
            QMessageBox.warning(self, "Não foi possível adicionar", str(erro))
            return

        self.campo_nova_condicao.clear()
        self._recarregar_lista()

    def remover_condicao(self):
        item = self.lista_condicoes.currentItem()
        if item is None:
            QMessageBox.warning(self, "Nenhuma seleção", "Selecione uma condição da lista para remover.")
            return

        self.controller.remover_condicao_produto(item.data(Qt.UserRole))
        self._recarregar_lista()
