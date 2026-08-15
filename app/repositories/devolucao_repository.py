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