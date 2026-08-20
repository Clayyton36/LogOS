from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QTextEdit,
    QPushButton,
    QMessageBox,
)

from app.controllers.devolucao_controller import (
    ACESSORIOS_VALIDOS,
    AVARIA_VALIDOS,
    DevolucaoController,
    DevolucaoValidationError,
)
from app.controllers.configuracoes_controller import ConfiguracoesController


class AnalisePage(QWidget):

    def __init__(self, controller: DevolucaoController = None, controller_configuracoes: ConfiguracoesController = None):
        super().__init__()

        self.controller = controller or DevolucaoController()
        self.controller_configuracoes = controller_configuracoes or ConfiguracoesController()
        self._pendentes = []

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)

        titulo = QLabel("Análise")
        titulo.setObjectName("tituloPagina")
        layout.addWidget(titulo)

        self.aviso_sem_pendentes = QLabel("Nenhuma devolução pendente de análise no momento.")
        self.aviso_sem_pendentes.setVisible(False)
        layout.addWidget(self.aviso_sem_pendentes)

        form = QFormLayout()

        self.combo_devolucao = QComboBox()
        self.combo_devolucao.currentIndexChanged.connect(self._atualizar_dados_devolucao_selecionada)
        form.addRow("Devolução pendente *", self.combo_devolucao)

        self.label_resumo = QLabel("")
        self.label_resumo.setWordWrap(True)
        form.addRow("Resumo do recebimento", self.label_resumo)

        self.combo_condicao = QComboBox()
        form.addRow("Condição do produto *", self.combo_condicao)

        self.combo_avaria = QComboBox()
        self.combo_avaria.addItem("")
        self.combo_avaria.addItems(AVARIA_VALIDOS)
        form.addRow("Avaria", self.combo_avaria)

        self.combo_acessorios = QComboBox()
        self.combo_acessorios.addItem("")
        self.combo_acessorios.addItems(ACESSORIOS_VALIDOS)
        form.addRow("Acessórios", self.combo_acessorios)

        self.campo_situacao_encontrada = QTextEdit()
        form.addRow("Situação encontrada", self.campo_situacao_encontrada)

        layout.addLayout(form)

        self.botao_registrar = QPushButton("Registrar Análise")
        self.botao_registrar.clicked.connect(self.registrar_analise)
        layout.addWidget(self.botao_registrar)

        self.setLayout(layout)

        self.ao_exibir()

    def ao_exibir(self):
        """Chamado pela MainWindow toda vez que a página é aberta, para
        trazer devoluções recebidas desde a última visita."""
        self._recarregar_condicoes_produto()

        devolucao_selecionada_id = self.combo_devolucao.currentData()

        self._pendentes = self.controller.listar_pendentes_analise()

        self.combo_devolucao.blockSignals(True)
        self.combo_devolucao.clear()
        for devolucao in self._pendentes:
            rotulo = f"{devolucao.numero_pedido} — {devolucao.cliente} ({devolucao.plataforma})"
            self.combo_devolucao.addItem(rotulo, devolucao.id)

        indice = self.combo_devolucao.findData(devolucao_selecionada_id)
        self.combo_devolucao.setCurrentIndex(indice if indice >= 0 else 0)
        self.combo_devolucao.blockSignals(False)

        tem_pendentes = len(self._pendentes) > 0
        self.aviso_sem_pendentes.setVisible(not tem_pendentes)
        self.combo_devolucao.setEnabled(tem_pendentes)
        self.botao_registrar.setEnabled(tem_pendentes)

        self._atualizar_dados_devolucao_selecionada()

    def _recarregar_condicoes_produto(self):
        condicao_selecionada = self.combo_condicao.currentText()

        self.combo_condicao.clear()
        self.combo_condicao.addItems(
            [condicao["nome"] for condicao in self.controller_configuracoes.listar_condicoes_produto()]
        )

        indice = self.combo_condicao.findText(condicao_selecionada)
        self.combo_condicao.setCurrentIndex(indice if indice >= 0 else 0)

    def selecionar_devolucao(self, devolucao_id):
        """Chamado pela MainWindow para abrir a página já com um pedido
        específico escolhido (ex.: vindo de um card do Dashboard)."""
        self.ao_exibir()
        indice = self.combo_devolucao.findData(devolucao_id)
        if indice >= 0:
            self.combo_devolucao.setCurrentIndex(indice)

    def _devolucao_selecionada(self):
        devolucao_id = self.combo_devolucao.currentData()
        return next((d for d in self._pendentes if d.id == devolucao_id), None)

    def _atualizar_dados_devolucao_selecionada(self):
        # Troca de devolução selecionada: limpa o formulário para não
        # arrastar dados digitados para a devolução anterior e enviá-los
        # por engano para a devolução errada.
        self._limpar_formulario()

        devolucao = self._devolucao_selecionada()
        if devolucao is None:
            self.label_resumo.setText("")
            return

        self.label_resumo.setText(
            f"SKU {devolucao.sku or '-'} · {devolucao.produto or '-'} · "
            f"recebido em {devolucao.data_recebimento or '-'} "
            f"por {devolucao.responsavel_recebimento or '-'}"
        )

    def registrar_analise(self):
        devolucao = self._devolucao_selecionada()

        try:
            self.controller.registrar_analise(
                devolucao_id=devolucao.id if devolucao else None,
                condicao_produto=self.combo_condicao.currentText(),
                avaria=self.combo_avaria.currentText(),
                acessorios=self.combo_acessorios.currentText(),
                situacao_encontrada=self.campo_situacao_encontrada.toPlainText(),
            )
        except DevolucaoValidationError as erro:
            QMessageBox.warning(self, "Dados incompletos", str(erro))
            return

        QMessageBox.information(self, "Sucesso", "Análise registrada com sucesso.")
        self.ao_exibir()

    def _limpar_formulario(self):
        self.combo_condicao.setCurrentIndex(0)
        self.combo_avaria.setCurrentIndex(0)
        self.combo_acessorios.setCurrentIndex(0)
        self.campo_situacao_encontrada.clear()
