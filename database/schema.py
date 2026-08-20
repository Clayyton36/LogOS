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
            condicao_produto TEXT,
            avaria TEXT,
            acessorios TEXT,
            situacao_encontrada TEXT,
            observacoes_analise TEXT,
            data_analise TEXT,
            observacoes_decisao TEXT,
            data_decisao TEXT,
            lancado_sistema TEXT DEFAULT 'NAO',
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Bancos criados antes de algum desses campos existir não ganham a
    # coluna via CREATE TABLE IF NOT EXISTS, então garantimos aqui.
    colunas_novas = [
        "responsavel_recebimento",
        "condicao_produto",
        "avaria",
        "acessorios",
        "situacao_encontrada",
        "observacoes_analise",
        "data_analise",
        "observacoes_decisao",
        "data_decisao",
    ]
    colunas_existentes = {row["name"] for row in cursor.execute("PRAGMA table_info(devolucoes)")}
    for coluna in colunas_novas:
        if coluna not in colunas_existentes:
            cursor.execute(f"ALTER TABLE devolucoes ADD COLUMN {coluna} TEXT")

    # lancado_sistema tem DEFAULT proprio (o SQLite usa esse default pra
    # preencher retroativamente as linhas ja existentes ao adicionar a
    # coluna, diferente das colunas acima que nascem NULL).
    if "lancado_sistema" not in colunas_existentes:
        cursor.execute("ALTER TABLE devolucoes ADD COLUMN lancado_sistema TEXT DEFAULT 'NAO'")

    tabela_condicoes_ja_existia = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='condicoes_produto'"
    ).fetchone() is not None

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS condicoes_produto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        )
    """)

    if not tabela_condicoes_ja_existia:
        cursor.executemany(
            "INSERT INTO condicoes_produto (nome) VALUES (?)",
            [
                ("Perfeito estado",),
                ("Bom estado - uso normal",),
                ("Avariado",),
                ("Incompleto",),
            ]
        )

    conn.commit()
    conn.close()