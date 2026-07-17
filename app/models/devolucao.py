from dataclasses import dataclass
from typing import Optional


@dataclass
class Devolucao:
    id: Optional[int] = None
    numero_pedido: str = ""
    numero_nf: str = ""
    cliente: str = ""
    plataforma: str = ""
    sku: str = ""
    produto: str = ""
    status: str = ""
    destino: str = ""
    data_recebimento: str = ""
    observacoes: str = ""
    data_criacao: str = ""
    data_atualizacao: str = ""