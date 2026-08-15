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
            responsavel_recebimento TEXT,
            status TEXT,
            destino TEXT,
            data_recebimento TEXT,
            observacoes TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Bancos criados antes do campo responsavel_recebimento existir não
    # ganham a coluna via CREATE TABLE IF NOT EXISTS, então garantimos aqui.
    colunas = {row["name"] for row in cursor.execute("PRAGMA table_info(devolucoes)")}
    if "responsavel_recebimento" not in colunas:
        cursor.execute("ALTER TABLE devolucoes ADD COLUMN responsavel_recebimento TEXT")

    conn.commit()
    conn.close()