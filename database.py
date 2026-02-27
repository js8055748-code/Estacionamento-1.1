import sqlite3
from datetime import datetime  # se você usar em outro lugar, pode manter


DB_NAME = "estacionamento.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()

    # tabela clientes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            placa TEXT NOT NULL,
            tipo TEXT NOT NULL,
            valor REAL DEFAULT 0
        )
    """)

    # tabela movimentacoes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL,
            entrada TEXT NOT NULL,
            saida TEXT,
            valor REAL
        )
    """)

    conn.commit()
    conn.close()
