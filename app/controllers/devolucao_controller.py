from datetime import datetime

from app.models.devolucao import Devolucao
from app.repositories.devolucao_repository import DevolucaoRepository


class DevolucaoValidationError(Exception):
    pass


class DevolucaoController:

    def __init__(self, repository: DevolucaoRepository = None):
        self.repository = repository or DevolucaoRepository()

    def registrar_recebimento(
        self,
        numero_pedido: str,
        plataforma: str,
        cliente: str,
        sku: str,
        produto: str,
        responsavel_recebimento: str,
        observacoes: str = "",
    ) -> int:
        campos_obrigatorios = {
            "Número do pedido": numero_pedido,
            "Plataforma": plataforma,
            "Cliente": cliente,
            "Responsável pelo recebimento": responsavel_recebimento,
        }
        faltando = [nome for nome, valor in campos_obrigatorios.items() if not valor.strip()]
        if faltando:
            raise DevolucaoValidationError(
                "Preencha os campos obrigatórios: " + ", ".join(faltando)
            )

        devolucao = Devolucao(
            numero_pedido=numero_pedido.strip(),
            plataforma=plataforma.strip(),
            cliente=cliente.strip(),
            sku=sku.strip(),
            produto=produto.strip(),
            responsavel_recebimento=responsavel_recebimento.strip(),
            observacoes=observacoes.strip(),
            status="Recebida",
            data_recebimento=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        return self.repository.salvar(devolucao)

    def consultar(self, termo_busca: str = "", plataforma: str = ""):
        return self.repository.listar(termo_busca=termo_busca.strip(), plataforma=plataforma.strip())

    def listar_plataformas(self):
        return self.repository.listar_plataformas()
