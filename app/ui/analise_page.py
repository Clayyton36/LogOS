from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QMessageBox,
)

from app.controllers.devolucao_controller import DevolucaoController, DevolucaoValidationError

CONDICOES_PRODUTO = [
    "Perfeito estado",
    "Bom estado - uso normal",
    "Avariado",
    "Incompleto",
]


class AnalisePage(QWidget):

    def __init__(self, controller: DevolucaoController = None):
        super().__init__()

        self.controller = controller or DevolucaoController()
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
        self.combo_condicao.addItems(CONDICOES_PRODUTO)
        form.addRow("Condição do produto *", self.combo_condicao)

        self.campo_avaria = QLineEdit()
        form.addRow("Avaria", self.campo_avaria)

        self.campo_acessorios = QLineEdit()
        form.addRow("Acessórios", self.campo_acessorios)

        self.campo_situacao_encontrada = QTextEdit()
        form.addRow("Situação encontrada", self.campo_situacao_encontrada)

        self.campo_observacoes = QTextEdit()
        form.addRow("Observações", self.campo_observacoes)

        layout.addLayout(form)

        self.botao_registrar = QPushButton("Registrar Análise")
        self.botao_registrar.clicked.connect(self.registrar_analise)
        layout.addWidget(self.botao_registrar)

        self.setLayout(layout)

        self.ao_exibir()

    def ao_exibir(self):
        """Chamado pela MainWindow toda vez que a página é aberta, para
        trazer devoluções recebidas desde a última visita."""
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

    def _devolucao_selecionada(self):
        devolucao_id = self.combo_devolucao.currentData()
        return next((d for d in self._pendentes if d.id == devolucao_id), None)

    def _atualizar_dados_devolucao_selecionada(self):
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
                avaria=self.campo_avaria.text(),
                acessorios=self.campo_acessorios.text(),
                situacao_encontrada=self.campo_situacao_encontrada.toPlainText(),
                observacoes_analise=self.campo_observacoes.toPlainText(),
            )
        except DevolucaoValidationError as erro:
            QMessageBox.warning(self, "Dados incompletos", str(erro))
            return

        QMessageBox.information(self, "Sucesso", "Análise registrada com sucesso.")
        self._limpar_formulario()
        self.ao_exibir()

    def _limpar_formulario(self):
        self.combo_condicao.setCurrentIndex(0)
        self.campo_avaria.clear()
        self.campo_acessorios.clear()
        self.campo_situacao_encontrada.clear()
        self.campo_observacoes.clear()
