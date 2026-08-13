import sqlite3

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")

    return g.db


def close_db(exception=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS materiais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            unidade_medida TEXT NOT NULL,
            quantidade REAL NOT NULL DEFAULT 0 CHECK (quantidade >= 0),
            estoque_minimo REAL NOT NULL DEFAULT 0 CHECK (estoque_minimo >= 0),
            localizacao TEXT,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'saida')),
            quantidade REAL NOT NULL CHECK (quantidade > 0),
            responsavel TEXT NOT NULL,
            observacao TEXT,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (material_id) REFERENCES materiais (id)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
        );

        CREATE INDEX IF NOT EXISTS idx_materiais_nome
            ON materiais (nome);

        CREATE INDEX IF NOT EXISTS idx_movimentacoes_material
            ON movimentacoes (material_id);

        CREATE INDEX IF NOT EXISTS idx_movimentacoes_data
            ON movimentacoes (criado_em);
        """
    )

    db.commit()
