from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.controllers.devolucao_controller import (
    OBSERVACOES_RECEBIMENTO_VALIDAS,
    PLATAFORMAS_VALIDAS,
    DevolucaoController,
    DevolucaoValidationError,
)


class NovaDevolucaoPage(QWidget):
    def __init__(self, controller: DevolucaoController = None):
        super().__init__()

        self.controller = controller or DevolucaoController()

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)

        titulo = QLabel("Nova Devolução")
        titulo.setObjectName("tituloPagina")
        layout.addWidget(titulo)

        form = QFormLayout()

        self.campo_numero_pedido = QLineEdit()
        self.campo_numero_nf = QLineEdit()
        self.combo_plataforma = QComboBox()
        self.combo_plataforma.addItems(PLATAFORMAS_VALIDAS)
        self.campo_cliente = QLineEdit()
        self.campo_produto = QLineEdit()
        self.campo_responsavel = QLineEdit()
        self.combo_observacoes = QComboBox()
        self.combo_observacoes.addItem("")
        self.combo_observacoes.addItems(OBSERVACOES_RECEBIMENTO_VALIDAS)

        form.addRow("Número do pedido *", self.campo_numero_pedido)
        form.addRow("Número da NF", self.campo_numero_nf)
        form.addRow("Plataforma *", self.combo_plataforma)
        form.addRow("Cliente *", self.campo_cliente)
        form.addRow("Produto", self.campo_produto)
        form.addRow("Responsável pelo recebimento *", self.campo_responsavel)
        form.addRow("Observações", self.combo_observacoes)

        layout.addLayout(form)

        botao_registrar = QPushButton("Registrar Recebimento")
        botao_registrar.clicked.connect(self.registrar_recebimento)
        layout.addWidget(botao_registrar)

        self.setLayout(layout)

    def registrar_recebimento(self):
        try:
            self.controller.registrar_recebimento(
                numero_pedido=self.campo_numero_pedido.text(),
                plataforma=self.combo_plataforma.currentText(),
                cliente=self.campo_cliente.text(),
                produto=self.campo_produto.text(),
                responsavel_recebimento=self.campo_responsavel.text(),
                numero_nf=self.campo_numero_nf.text(),
                observacoes=self.combo_observacoes.currentText(),
            )
        except DevolucaoValidationError as erro:
            QMessageBox.warning(self, "Dados incompletos", str(erro))
            return

        QMessageBox.information(self, "Sucesso", "Devolução registrada com sucesso.")
        self._limpar_formulario()

    def _limpar_formulario(self):
        self.campo_numero_pedido.clear()
        self.campo_numero_nf.clear()
        self.combo_plataforma.setCurrentIndex(0)
        self.campo_cliente.clear()
        self.campo_produto.clear()
        self.campo_responsavel.clear()
        self.combo_observacoes.setCurrentIndex(0)
