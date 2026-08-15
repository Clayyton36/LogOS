from database.connection import get_connection
from app.models.devolucao import Devolucao


class DevolucaoRepository:

    def salvar(self, devolucao: Devolucao):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO devolucoes (
                numero_pedido,
                numero_nf,
                cliente,
                plataforma,
                sku,
                produto,
                responsavel_recebimento,
                status,
                destino,
                data_recebimento,
                observacoes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            devolucao.numero_pedido,
            devolucao.numero_nf,
            devolucao.cliente,
            devolucao.plataforma,
            devolucao.sku,
            devolucao.produto,
            devolucao.responsavel_recebimento,
            devolucao.status,
            devolucao.destino,
            devolucao.data_recebimento,
            devolucao.observacoes
        ))

        conn.commit()
        devolucao_id = cursor.lastrowid
        conn.close()
        return devolucao_id

    def listar(self, termo_busca: str = "", plataforma: str = ""):
        conn = get_connection()
        cursor = conn.cursor()

        condicoes = []
        parametros = []

        if termo_busca:
            condicoes.append("(numero_pedido LIKE ? OR cliente LIKE ?)")
            curinga = f"%{termo_busca}%"
            parametros.extend([curinga, curinga])

        if plataforma:
            condicoes.append("plataforma = ?")
            parametros.append(plataforma)

        query = "SELECT * FROM devolucoes"
        if condicoes:
            query += " WHERE " + " AND ".join(condicoes)
        query += " ORDER BY data_criacao DESC"

        cursor.execute(query, parametros)
        linhas = cursor.fetchall()
        conn.close()

        return [Devolucao(**dict(linha)) for linha in linhas]

    def listar_plataformas(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT DISTINCT plataforma FROM devolucoes "
            "WHERE plataforma != '' ORDER BY plataforma"
        )
        linhas = cursor.fetchall()
        conn.close()

        return [linha["plataforma"] for linha in linhas]

    def listar_por_status(self, status: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM devolucoes WHERE status = ? ORDER BY data_recebimento ASC",
            (status,)
        )
        linhas = cursor.fetchall()
        conn.close()

        return [Devolucao(**dict(linha)) for linha in linhas]

    def atualizar_analise(
        self,
        devolucao_id: int,
        condicao_produto: str,
        avaria: str,
        acessorios: str,
        situacao_encontrada: str,
        observacoes_analise: str,
        data_analise: str,
        novo_status: str,
    ):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE devolucoes
            SET condicao_produto = ?,
                avaria = ?,
                acessorios = ?,
                situacao_encontrada = ?,
                observacoes_analise = ?,
                data_analise = ?,
                status = ?,
                data_atualizacao = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            condicao_produto,
            avaria,
            acessorios,
            situacao_encontrada,
            observacoes_analise,
            data_analise,
            novo_status,
            devolucao_id,
        ))

        conn.commit()
        conn.close()