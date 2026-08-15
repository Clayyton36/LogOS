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

from app.controllers.devolucao_controller import DevolucaoController

COLUNAS = ["Pedido", "Cliente", "Plataforma", "Status", "Destino", "Recebido em"]


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
        layout.addWidget(self.tabela)

        rodape = QHBoxLayout()
        self.label_contagem = QLabel("")
        self.label_contagem.setStyleSheet("color: #6b7280; font-size: 12px;")
        rodape.addWidget(self.label_contagem)
        rodape.addStretch()

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

        self._devolucoes_exibidas = self.controller.consultar(termo_busca=termo, plataforma=plataforma)
        self._preencher_tabela(self._devolucoes_exibidas)

        quantidade = len(self._devolucoes_exibidas)
        self.label_contagem.setText(
            "1 devolução encontrada" if quantidade == 1 else f"{quantidade} devoluções encontradas"
        )

    def _preencher_tabela(self, devolucoes):
        self.tabela.setRowCount(len(devolucoes))
        for linha, devolucao in enumerate(devolucoes):
            valores = [
                devolucao.numero_pedido,
                devolucao.cliente,
                devolucao.plataforma,
                devolucao.status,
                devolucao.destino,
                devolucao.data_recebimento,
            ]
            for coluna, valor in enumerate(valores):
                self.tabela.setItem(linha, coluna, QTableWidgetItem(valor or ""))

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

        try:
            quantidade = self.controller.exportar_para_excel(
                caminho, termo_busca=termo, plataforma=plataforma
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
