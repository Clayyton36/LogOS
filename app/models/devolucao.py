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
    responsavel_recebimento: str = ""
    status: str = ""
    destino: str = ""
    data_recebimento: str = ""
    observacoes: str = ""
    condicao_produto: str = ""
    avaria: str = ""
    acessorios: str = ""
    situacao_encontrada: str = ""
    observacoes_analise: str = ""
    data_analise: str = ""
    data_criacao: str = ""
    data_atualizacao: str = ""