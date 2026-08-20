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

from app.controllers.devolucao_controller import DESTINOS_VALIDOS, DevolucaoController, DevolucaoValidationError


class DecisaoPage(QWidget):

    def __init__(self, controller: DevolucaoController = None):
        super().__init__()

        self.controller = controller or DevolucaoController()
        self._pendentes = []

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)

        titulo = QLabel("Decisão")
        titulo.setObjectName("tituloPagina")
        layout.addWidget(titulo)

        self.aviso_sem_pendentes = QLabel("Nenhuma devolução pendente de decisão no momento.")
        self.aviso_sem_pendentes.setVisible(False)
        layout.addWidget(self.aviso_sem_pendentes)

        form = QFormLayout()

        self.combo_devolucao = QComboBox()
        self.combo_devolucao.currentIndexChanged.connect(self._atualizar_dados_devolucao_selecionada)
        form.addRow("Devolução pendente *", self.combo_devolucao)

        self.label_resumo = QLabel("")
        self.label_resumo.setWordWrap(True)
        form.addRow("Resultado da análise", self.label_resumo)

        self.combo_destino = QComboBox()
        self.combo_destino.addItems(DESTINOS_VALIDOS)
        form.addRow("Destino *", self.combo_destino)

        self.campo_observacoes = QTextEdit()
        form.addRow("Observações", self.campo_observacoes)

        layout.addLayout(form)

        self.botao_registrar = QPushButton("Registrar Decisão")
        self.botao_registrar.clicked.connect(self.registrar_decisao)
        layout.addWidget(self.botao_registrar)

        self.setLayout(layout)

        self.ao_exibir()

    def ao_exibir(self):
        """Chamado pela MainWindow toda vez que a página é aberta, para
        trazer devoluções analisadas desde a última visita."""
        devolucao_selecionada_id = self.combo_devolucao.currentData()

        self._pendentes = self.controller.listar_pendentes_decisao()

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
        self.combo_destino.setEnabled(tem_pendentes)
        self.botao_registrar.setEnabled(tem_pendentes)

        self._atualizar_dados_devolucao_selecionada()

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
            f"Condição: {devolucao.condicao_produto or '-'} · "
            f"Avaria: {devolucao.avaria or '-'} · "
            f"Situação encontrada: {devolucao.situacao_encontrada or '-'}"
        )

    def registrar_decisao(self):
        devolucao = self._devolucao_selecionada()

        try:
            self.controller.registrar_decisao(
                devolucao_id=devolucao.id if devolucao else None,
                destino=self.combo_destino.currentText(),
                observacoes_decisao=self.campo_observacoes.toPlainText(),
            )
        except DevolucaoValidationError as erro:
            QMessageBox.warning(self, "Dados incompletos", str(erro))
            return

        QMessageBox.information(self, "Sucesso", "Decisão registrada com sucesso.")
        self.ao_exibir()

    def _limpar_formulario(self):
        self.combo_destino.setCurrentIndex(0)
        self.campo_observacoes.clear()
