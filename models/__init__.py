from database import get_db


def listar_materiais():
    return get_db().execute(
        """
        SELECT *
        FROM materiais
        ORDER BY nome
        """
    ).fetchall()


def buscar_material(material_id):
    return get_db().execute(
        """
        SELECT *
        FROM materiais
        WHERE id = ?
        """,
        (material_id,),
    ).fetchone()


def buscar_material_por_codigo(codigo):
    return get_db().execute(
        """
        SELECT *
        FROM materiais
        WHERE codigo = ?
        """,
        (codigo,),
    ).fetchone()


def criar_material(
    codigo,
    nome,
    categoria,
    unidade_medida,
    quantidade,
    estoque_minimo,
    localizacao,
):
    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO materiais (
            codigo,
            nome,
            categoria,
            unidade_medida,
            quantidade,
            estoque_minimo,
            localizacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            codigo,
            nome,
            categoria,
            unidade_medida,
            quantidade,
            estoque_minimo,
            localizacao,
        ),
    )

    db.commit()
    return cursor.lastrowid


def atualizar_material(
    material_id,
    codigo,
    nome,
    categoria,
    unidade_medida,
    quantidade,
    estoque_minimo,
    localizacao,
):
    db = get_db()

    db.execute(
        """
        UPDATE materiais
        SET codigo = ?,
            nome = ?,
            categoria = ?,
            unidade_medida = ?,
            quantidade = ?,
            estoque_minimo = ?,
            localizacao = ?,
            atualizado_em = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            codigo,
            nome,
            categoria,
            unidade_medida,
            quantidade,
            estoque_minimo,
            localizacao,
            material_id,
        ),
    )

    db.commit()


def excluir_material(material_id):
    db = get_db()
    db.execute(
        "DELETE FROM materiais WHERE id = ?",
        (material_id,),
    )
    db.commit()
