from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QFileDialog,
    QMessageBox,
)

from app.controllers.devolucao_controller import DevolucaoController, DevolucaoValidationError

COLUNAS = ["Pedido", "Cliente", "Plataforma", "Status", "Destino", "Recebido em", "Lançado no sistema"]


class RelatoriosPage(QWidget):

    def __init__(self, controller: DevolucaoController = None):
        super().__init__()

        self.controller = controller or DevolucaoController()
        self._devolucoes_exibidas = []

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)

        titulo = QLabel("Relatórios")
        titulo.setObjectName("tituloPagina")
        layout.addWidget(titulo)

        filtros = QHBoxLayout()

        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Buscar por número do pedido ou cliente")
        self.campo_busca.returnPressed.connect(self.buscar)
        filtros.addWidget(self.campo_busca)

        self.combo_plataforma = QComboBox()
        self.combo_plataforma.addItem("Todas as plataformas", "")
        self.combo_plataforma.currentIndexChanged.connect(self.buscar)
        filtros.addWidget(self.combo_plataforma)

        self.combo_lancado_sistema = QComboBox()
        self.combo_lancado_sistema.addItem("Todos", "")
        self.combo_lancado_sistema.addItem("Lançados no sistema", "SIM")
        self.combo_lancado_sistema.addItem("Não lançados no sistema", "NAO")
        self.combo_lancado_sistema.currentIndexChanged.connect(self.buscar)
        filtros.addWidget(self.combo_lancado_sistema)

        botao_buscar = QPushButton("Buscar")
        botao_buscar.clicked.connect(self.buscar)
        filtros.addWidget(botao_buscar)

        layout.addLayout(filtros)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(len(COLUNAS))
        self.tabela.setHorizontalHeaderLabels(COLUNAS)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.itemSelectionChanged.connect(self._atualizar_botao_lancado)
        layout.addWidget(self.tabela)

        rodape = QHBoxLayout()
        self.label_contagem = QLabel("")
        self.label_contagem.setStyleSheet("color: #6b7280; font-size: 12px;")
        rodape.addWidget(self.label_contagem)
        rodape.addStretch()

        self.botao_alternar_lancado = QPushButton("Marcar como lançado")
        self.botao_alternar_lancado.setEnabled(False)
        self.botao_alternar_lancado.clicked.connect(self._alternar_lancado_sistema)
        rodape.addWidget(self.botao_alternar_lancado)

        botao_exportar = QPushButton("Exportar para Excel")
        botao_exportar.clicked.connect(self.exportar)
        rodape.addWidget(botao_exportar)

        layout.addLayout(rodape)

        self.setLayout(layout)

        self.ao_exibir()

    def ao_exibir(self):
        """Chamado pela MainWindow toda vez que a página é aberta, para
        trazer devoluções registradas desde a última visita."""
        self._atualizar_combo_plataformas()
        self.buscar()

    def _atualizar_combo_plataformas(self):
        plataforma_selecionada = self.combo_plataforma.currentData()

        self.combo_plataforma.blockSignals(True)
        self.combo_plataforma.clear()
        self.combo_plataforma.addItem("Todas as plataformas", "")
        for plataforma in self.controller.listar_plataformas():
            self.combo_plataforma.addItem(plataforma, plataforma)

        indice = self.combo_plataforma.findData(plataforma_selecionada)
        self.combo_plataforma.setCurrentIndex(indice if indice >= 0 else 0)
        self.combo_plataforma.blockSignals(False)

    def buscar(self):
        termo = self.campo_busca.text().strip()
        plataforma = self.combo_plataforma.currentData() or ""
        lancado_sistema = self.combo_lancado_sistema.currentData() or ""

        self._devolucoes_exibidas = self.controller.consultar(
            termo_busca=termo, plataforma=plataforma, lancado_sistema=lancado_sistema
        )
        self._preencher_tabela(self._devolucoes_exibidas)
        self._atualizar_botao_lancado()

        quantidade = len(self._devolucoes_exibidas)
        self.label_contagem.setText(
            "1 devolução encontrada" if quantidade == 1 else f"{quantidade} devoluções encontradas"
        )

    def _preencher_tabela(self, devolucoes):
        self.tabela.setRowCount(len(devolucoes))
        for linha, devolucao in enumerate(devolucoes):
            lancado = "SIM" if (devolucao.lancado_sistema or "NAO") == "SIM" else "NÃO"
            valores = [
                devolucao.numero_pedido,
                devolucao.cliente,
                devolucao.plataforma,
                devolucao.status,
                devolucao.destino,
                devolucao.data_recebimento,
                lancado,
            ]
            for coluna, valor in enumerate(valores):
                self.tabela.setItem(linha, coluna, QTableWidgetItem(valor or ""))

    def _atualizar_botao_lancado(self):
        linha = self.tabela.currentRow()
        if linha < 0 or linha >= len(self._devolucoes_exibidas):
            self.botao_alternar_lancado.setEnabled(False)
            self.botao_alternar_lancado.setText("Marcar como lançado")
            return

        devolucao = self._devolucoes_exibidas[linha]
        self.botao_alternar_lancado.setEnabled(True)
        if (devolucao.lancado_sistema or "NAO") == "SIM":
            self.botao_alternar_lancado.setText("Desmarcar lançamento")
        else:
            self.botao_alternar_lancado.setText("Marcar como lançado")

    def _alternar_lancado_sistema(self):
        linha = self.tabela.currentRow()
        if linha < 0 or linha >= len(self._devolucoes_exibidas):
            return

        devolucao = self._devolucoes_exibidas[linha]
        novo_valor = "NAO" if (devolucao.lancado_sistema or "NAO") == "SIM" else "SIM"

        try:
            self.controller.marcar_lancado_sistema(devolucao.id, novo_valor)
        except DevolucaoValidationError as erro:
            QMessageBox.warning(self, "Não foi possível atualizar", str(erro))
            return

        self.buscar()

    def exportar(self):
        caminho, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar relatório",
            "devolucoes.xlsx",
            "Planilha Excel (*.xlsx)",
        )
        if not caminho:
            return

        termo = self.campo_busca.text().strip()
        plataforma = self.combo_plataforma.currentData() or ""
        lancado_sistema = self.combo_lancado_sistema.currentData() or ""

        try:
            quantidade = self.controller.exportar_para_excel(
                caminho, termo_busca=termo, plataforma=plataforma, lancado_sistema=lancado_sistema
            )
        except OSError as erro:
            QMessageBox.critical(
                self, "Erro ao exportar",
                f"Não foi possível salvar o arquivo. Verifique se ele não está aberto em outro programa.\n\n{erro}"
            )
            return

        QMessageBox.information(
            self, "Exportado",
            f"{quantidade} devolução(ões) exportada(s) para:\n{caminho}"
        )
