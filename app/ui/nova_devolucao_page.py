from PySide6.QtWidgets import (
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.controllers.devolucao_controller import DevolucaoController, DevolucaoValidationError


class NovaDevolucaoPage(QWidget):
    def __init__(self, controller: DevolucaoController = None):
        super().__init__()

        self.controller = controller or DevolucaoController()

        layout = QVBoxLayout()

        titulo = QLabel("Nova Devolução")
        layout.addWidget(titulo)

        form = QFormLayout()

        self.campo_numero_pedido = QLineEdit()
        self.campo_plataforma = QLineEdit()
        self.campo_cliente = QLineEdit()
        self.campo_sku = QLineEdit()
        self.campo_produto = QLineEdit()
        self.campo_responsavel = QLineEdit()
        self.campo_observacoes = QTextEdit()

        form.addRow("Número do pedido *", self.campo_numero_pedido)
        form.addRow("Plataforma *", self.campo_plataforma)
        form.addRow("Cliente *", self.campo_cliente)
        form.addRow("SKU", self.campo_sku)
        form.addRow("Produto", self.campo_produto)
        form.addRow("Responsável pelo recebimento *", self.campo_responsavel)
        form.addRow("Observações", self.campo_observacoes)

        layout.addLayout(form)

        botao_registrar = QPushButton("Registrar Recebimento")
        botao_registrar.clicked.connect(self.registrar_recebimento)
        layout.addWidget(botao_registrar)

        self.setLayout(layout)

    def registrar_recebimento(self):
        try:
            self.controller.registrar_recebimento(
                numero_pedido=self.campo_numero_pedido.text(),
                plataforma=self.campo_plataforma.text(),
                cliente=self.campo_cliente.text(),
                sku=self.campo_sku.text(),
                produto=self.campo_produto.text(),
                responsavel_recebimento=self.campo_responsavel.text(),
                observacoes=self.campo_observacoes.toPlainText(),
            )
        except DevolucaoValidationError as erro:
            QMessageBox.warning(self, "Dados incompletos", str(erro))
            return

        QMessageBox.information(self, "Sucesso", "Devolução registrada com sucesso.")
        self._limpar_formulario()

    def _limpar_formulario(self):
        self.campo_numero_pedido.clear()
        self.campo_plataforma.clear()
        self.campo_cliente.clear()
        self.campo_sku.clear()
        self.campo_produto.clear()
        self.campo_responsavel.clear()
        self.campo_observacoes.clear()
