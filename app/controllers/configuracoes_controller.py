import sqlite3

from app.repositories.condicao_produto_repository import CondicaoProdutoRepository


class ConfiguracaoValidationError(Exception):
    pass


class ConfiguracoesController:

    def __init__(self, repository: CondicaoProdutoRepository = None):
        self.repository = repository or CondicaoProdutoRepository()

    def listar_condicoes_produto(self):
        return self.repository.listar()

    def adicionar_condicao_produto(self, nome: str):
        nome = nome.strip()
        if not nome:
            raise ConfiguracaoValidationError("Informe um nome para a condição do produto.")

        try:
            self.repository.adicionar(nome)
        except sqlite3.IntegrityError:
            raise ConfiguracaoValidationError(f'A condição "{nome}" já existe.')

    def remover_condicao_produto(self, condicao_id: int):
        self.repository.remover(condicao_id)
