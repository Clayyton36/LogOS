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
    QMessageBox,
)

from app.controllers.devolucao_controller import DevolucaoController

COLUNAS = ["Pedido", "Cliente", "Plataforma", "SKU", "Produto", "Status", "Recebido em"]


class ConsultaPage(QWidget):

    def __init__(self, controller: DevolucaoController = None):
        super().__init__()

        self.controller = controller or DevolucaoController()
        self._devolucoes_exibidas = []

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)

        titulo = QLabel("Consulta")
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
        self.tabela.doubleClicked.connect(self.abrir_detalhes)
        layout.addWidget(self.tabela)

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

    def _preencher_tabela(self, devolucoes):
        self.tabela.setRowCount(len(devolucoes))
        for linha, devolucao in enumerate(devolucoes):
            valores = [
                devolucao.numero_pedido,
                devolucao.cliente,
                devolucao.plataforma,
                devolucao.sku,
                devolucao.produto,
                devolucao.status,
                devolucao.data_recebimento,
            ]
            for coluna, valor in enumerate(valores):
                self.tabela.setItem(linha, coluna, QTableWidgetItem(valor or ""))

    def abrir_detalhes(self, index):
        devolucao = self._devolucoes_exibidas[index.row()]
        detalhes = (
            f"Pedido: {devolucao.numero_pedido}\n"
            f"NF: {devolucao.numero_nf or '-'}\n"
            f"Cliente: {devolucao.cliente}\n"
            f"Plataforma: {devolucao.plataforma}\n"
            f"SKU: {devolucao.sku or '-'}\n"
            f"Produto: {devolucao.produto or '-'}\n"
            f"Responsável pelo recebimento: {devolucao.responsavel_recebimento or '-'}\n"
            f"Status: {devolucao.status or '-'}\n"
            f"Destino: {devolucao.destino or '-'}\n"
            f"Recebido em: {devolucao.data_recebimento or '-'}\n"
            f"Observações: {devolucao.observacoes or '-'}"
        )
        QMessageBox.information(self, f"Devolução #{devolucao.id}", detalhes)
