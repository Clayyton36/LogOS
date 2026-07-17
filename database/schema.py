from database.connection import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devolucoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_pedido TEXT,
            numero_nf TEXT,
            cliente TEXT NOT NULL,
            plataforma TEXT NOT NULL,
            sku TEXT,
            produto TEXT,
            status TEXT,
            destino TEXT,
            data_recebimento TEXT,
            observacoes TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()