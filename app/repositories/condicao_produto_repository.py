from database.connection import get_connection


class CondicaoProdutoRepository:

    def listar(self):
        conn = get_connection()
        try:
            linhas = conn.execute("SELECT id, nome FROM condicoes_produto ORDER BY id").fetchall()
            return [dict(linha) for linha in linhas]
        finally:
            conn.close()

    def adicionar(self, nome: str):
        conn = get_connection()
        try:
            conn.execute("INSERT INTO condicoes_produto (nome) VALUES (?)", (nome,))
            conn.commit()
        finally:
            conn.close()

    def remover(self, condicao_id: int):
        conn = get_connection()
        try:
            conn.execute("DELETE FROM condicoes_produto WHERE id = ?", (condicao_id,))
            conn.commit()
        finally:
            conn.close()
