from database.connection import get_connection
from app.models.devolucao import Devolucao


class DevolucaoRepository:

    def salvar(self, devolucao: Devolucao):
        conn = get_connection()
        try:
            cursor = conn.execute("""
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
            return cursor.lastrowid
        finally:
            conn.close()

    def listar(self, termo_busca: str = "", plataforma: str = ""):
        conn = get_connection()
        try:
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

            linhas = conn.execute(query, parametros).fetchall()
            return [Devolucao(**dict(linha)) for linha in linhas]
        finally:
            conn.close()

    def listar_plataformas(self):
        conn = get_connection()
        try:
            linhas = conn.execute(
                "SELECT DISTINCT plataforma FROM devolucoes "
                "WHERE plataforma != '' ORDER BY plataforma"
            ).fetchall()
            return [linha["plataforma"] for linha in linhas]
        finally:
            conn.close()

    def listar_por_status(self, status: str):
        conn = get_connection()
        try:
            linhas = conn.execute(
                "SELECT * FROM devolucoes WHERE status = ? ORDER BY data_recebimento ASC",
                (status,)
            ).fetchall()
            return [Devolucao(**dict(linha)) for linha in linhas]
        finally:
            conn.close()

    def obter_indicadores(self):
        conn = get_connection()
        try:
            linha = conn.execute("""
                SELECT
                    COUNT(*) AS total,
                    SUM(CASE WHEN status = 'Recebida' THEN 1 ELSE 0 END) AS recebidas,
                    SUM(CASE WHEN status = 'Analisada' THEN 1 ELSE 0 END) AS aguardando_decisao,
                    SUM(CASE WHEN status = 'Finalizada' AND destino = 'ESTOQUE' THEN 1 ELSE 0 END) AS estoque,
                    SUM(CASE WHEN status = 'Finalizada' AND destino = 'TROCA' THEN 1 ELSE 0 END) AS troca,
                    SUM(CASE WHEN status = 'Finalizada' AND destino = 'DESCARTE' THEN 1 ELSE 0 END) AS descarte
                FROM devolucoes
            """).fetchone()
            return {chave: (linha[chave] or 0) for chave in linha.keys()}
        finally:
            conn.close()

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
        try:
            conn.execute("""
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
        finally:
            conn.close()

    def atualizar_decisao(
        self,
        devolucao_id: int,
        destino: str,
        observacoes_decisao: str,
        data_decisao: str,
        novo_status: str,
    ):
        conn = get_connection()
        try:
            conn.execute("""
                UPDATE devolucoes
                SET destino = ?,
                    observacoes_decisao = ?,
                    data_decisao = ?,
                    status = ?,
                    data_atualizacao = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (
                destino,
                observacoes_decisao,
                data_decisao,
                novo_status,
                devolucao_id,
            ))
            conn.commit()
        finally:
            conn.close()