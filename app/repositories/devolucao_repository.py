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
                status,
                destino,
                data_recebimento,
                observacoes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            devolucao.numero_pedido,
            devolucao.numero_nf,
            devolucao.cliente,
            devolucao.plataforma,
            devolucao.sku,
            devolucao.produto,
            devolucao.status,
            devolucao.destino,
            devolucao.data_recebimento,
            devolucao.observacoes
        ))

        conn.commit()
        conn.close()