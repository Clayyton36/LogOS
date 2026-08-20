from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from app.controllers.devolucao_controller import DevolucaoController


class DetalheDevolucaoDialog(QDialog):

    def __init__(self, controller: DevolucaoController, devolucao, parent=None):
        super().__init__(parent)

        self.controller = controller
        self.devolucao = devolucao
        self.foi_reaberta = False

        self.setWindowTitle(f"Devolução #{devolucao.id} — {devolucao.numero_pedido}")
        self.setMinimumWidth(420)

        layout = QVBoxLayout()

        detalhes = (
            f"Pedido: {devolucao.numero_pedido}\n"
            f"NF: {devolucao.numero_nf or '-'}\n"
            f"Cliente: {devolucao.cliente}\n"
            f"Plataforma: {devolucao.plataforma}\n"
            f"Produto: {devolucao.produto or '-'}\n"
            f"Responsável pelo recebimento: {devolucao.responsavel_recebimento or '-'}\n"
            f"Recebido em: {devolucao.data_recebimento or '-'}\n"
            f"Condição do produto: {devolucao.condicao_produto or '-'}\n"
            f"Avaria: {devolucao.avaria or '-'}\n"
            f"Acessórios: {devolucao.acessorios or '-'}\n"
            f"Situação encontrada: {devolucao.situacao_encontrada or '-'}\n"
            f"Analisado em: {devolucao.data_analise or '-'}\n"
            f"Destino: {devolucao.destino or '-'}\n"
            f"Observações da decisão: {devolucao.observacoes_decisao or '-'}\n"
            f"Decidido em: {devolucao.data_decisao or '-'}\n"
            f"Status: {devolucao.status or '-'}"
        )
        label = QLabel(detalhes)
        label.setWordWrap(True)
        layout.addWidget(label)

        botoes = QHBoxLayout()

        botao_reabrir = QPushButton("Reabrir para nova decisão")
        botao_reabrir.clicked.connect(self._reabrir)
        botoes.addWidget(botao_reabrir)

        botao_fechar = QPushButton("Fechar")
        botao_fechar.clicked.connect(self.accept)
        botoes.addWidget(botao_fechar)

        layout.addLayout(botoes)
        self.setLayout(layout)

    def _reabrir(self):
        resposta = QMessageBox.question(
            self,
            "Reabrir devolução",
            f"Reabrir a devolução {self.devolucao.numero_pedido}? Ela sairá da contagem "
            "de finalizadas e voltará para a tela Decisão.",
        )
        if resposta != QMessageBox.Yes:
            return

        self.controller.reabrir_devolucao(self.devolucao.id)
        self.foi_reaberta = True

        QMessageBox.information(
            self,
            "Devolução reaberta",
            "A devolução foi reaberta e está disponível na tela Decisão.",
        )
        self.accept()
