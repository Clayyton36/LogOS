from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QDialog,
    QListWidget,
)

from app.controllers.devolucao_controller import DevolucaoController
from app.ui.detalhe_devolucao_dialog import DetalheDevolucaoDialog

# (chave do indicador, rótulo do tile, cor da faixa lateral)
# Recebidas/Aguardando decisão são dois estágios do mesmo fluxo (mesma cor,
# tons diferentes = ordem). Estoque/Troca/Descarte são o resultado final,
# por isso usam a paleta de status reservada (bom/atenção/crítico).
INDICADORES = [
    ("recebidas", "Recebidas · aguardando análise", "#60a5fa"),
    ("aguardando_decisao", "Analisadas · aguardando decisão", "#2563eb"),
    ("estoque", "Retornadas ao estoque", "#0ca30c"),
    ("troca", "Enviadas para troca", "#fab219"),
    ("descarte", "Descartadas", "#d03b3b"),
]


class TileIndicador(QFrame):
    clicado = Signal()

    def mousePressEvent(self, evento):
        if evento.button() == Qt.LeftButton:
            self.clicado.emit()
        super().mousePressEvent(evento)


def _criar_tile(cor: str) -> tuple[TileIndicador, QLabel, QLabel]:
    tile = TileIndicador()
    tile.setObjectName("tileIndicador")
    tile.setCursor(Qt.PointingHandCursor)
    tile.setStyleSheet(f"""
        #tileIndicador {{
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-left: 4px solid {cor};
            border-radius: 8px;
        }}
    """)

    layout = QVBoxLayout()
    layout.setContentsMargins(16, 14, 16, 14)
    layout.setSpacing(4)

    valor = QLabel("0")
    valor.setStyleSheet("font-size: 30px; font-weight: bold; color: #1f2937; border: none;")
    layout.addWidget(valor)

    rotulo = QLabel("")
    rotulo.setWordWrap(True)
    rotulo.setStyleSheet("font-size: 12px; color: #6b7280; border: none;")
    layout.addWidget(rotulo)

    tile.setLayout(layout)
    return tile, valor, rotulo


class DashboardPage(QWidget):

    def __init__(self, controller: DevolucaoController = None):
        super().__init__()

        self.controller = controller or DevolucaoController()
        self._labels_valor = {}
        self._abrir_analise = None
        self._abrir_decisao = None

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        cabecalho = QHBoxLayout()

        selo = QLabel("L")
        selo.setFixedSize(40, 40)
        selo.setAlignment(Qt.AlignCenter)
        selo.setStyleSheet("""
            background-color: #2563eb;
            color: #ffffff;
            border-radius: 20px;
            font-size: 18px;
            font-weight: bold;
        """)
        cabecalho.addWidget(selo)

        nome = QLabel("LogOS")
        nome.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #1f2937;
            margin-left: 10px;
        """)
        cabecalho.addWidget(nome)

        cabecalho.addStretch()
        layout.addLayout(cabecalho)

        indicadores = QHBoxLayout()
        indicadores.setSpacing(16)
        for chave, rotulo_texto, cor in INDICADORES:
            tile, label_valor, label_rotulo = _criar_tile(cor)
            label_rotulo.setText(rotulo_texto)
            tile.clicado.connect(
                lambda chave=chave, rotulo_texto=rotulo_texto: self._abrir_lista(chave, rotulo_texto)
            )
            indicadores.addWidget(tile)
            self._labels_valor[chave] = label_valor
        layout.addLayout(indicadores)

        layout.addStretch()

        self.setLayout(layout)

        self.ao_exibir()

    def definir_navegacao(self, abrir_analise=None, abrir_decisao=None):
        """Recebe da MainWindow as funções que trocam de página, para que o
        Dashboard consiga levar direto a um pedido específico em Análise ou
        Decisão sem precisar conhecer o QStackedWidget."""
        self._abrir_analise = abrir_analise
        self._abrir_decisao = abrir_decisao

    def ao_exibir(self):
        """Chamado pela MainWindow toda vez que a página é aberta, para
        manter os indicadores atualizados."""
        indicadores = self.controller.obter_indicadores()
        for chave, label_valor in self._labels_valor.items():
            label_valor.setText(str(indicadores.get(chave, 0)))

    def _abrir_lista(self, chave, rotulo_texto):
        devolucoes = self.controller.listar_por_indicador(chave)

        dialog = QDialog(self)
        dialog.setWindowTitle(rotulo_texto)
        dialog.setMinimumWidth(360)
        dialog.setMinimumHeight(320)

        layout = QVBoxLayout()

        if not devolucoes:
            layout.addWidget(QLabel("Nenhum pedido nesta contagem."))
        else:
            lista = QListWidget()
            for devolucao in devolucoes:
                lista.addItem(f"{devolucao.numero_pedido} — {devolucao.cliente}")

            def ao_clicar(item):
                devolucao_selecionada = devolucoes[lista.row(item)]
                dialog.accept()
                self._abrir_pedido(devolucao_selecionada)

            lista.itemClicked.connect(ao_clicar)
            layout.addWidget(lista)

        dialog.setLayout(layout)
        dialog.exec()

    def _abrir_pedido(self, devolucao):
        if devolucao.status == "Recebida" and self._abrir_analise:
            self._abrir_analise(devolucao.id)
        elif devolucao.status == "Analisada" and self._abrir_decisao:
            self._abrir_decisao(devolucao.id)
        else:
            dialog = DetalheDevolucaoDialog(self.controller, devolucao, self)
            dialog.exec()
            self.ao_exibir()
