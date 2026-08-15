from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)

from app.controllers.devolucao_controller import DevolucaoController

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


def _criar_tile(cor: str) -> tuple[QFrame, QLabel, QLabel]:
    tile = QFrame()
    tile.setObjectName("tileIndicador")
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
            indicadores.addWidget(tile)
            self._labels_valor[chave] = label_valor
        layout.addLayout(indicadores)

        layout.addStretch()

        self.setLayout(layout)

        self.ao_exibir()

    def ao_exibir(self):
        """Chamado pela MainWindow toda vez que a página é aberta, para
        manter os indicadores atualizados."""
        indicadores = self.controller.obter_indicadores()
        for chave, label_valor in self._labels_valor.items():
            label_valor.setText(str(indicadores.get(chave, 0)))
