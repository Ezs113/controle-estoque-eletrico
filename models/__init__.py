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


def listar_movimentacoes(limite=None):
    sql = """
        SELECT
            movimentacoes.*,
            materiais.codigo AS material_codigo,
            materiais.nome AS material_nome,
            materiais.unidade_medida
        FROM movimentacoes
        INNER JOIN materiais
            ON materiais.id = movimentacoes.material_id
        ORDER BY
            movimentacoes.data_movimentacao DESC,
            movimentacoes.id DESC
    """

    parametros = ()

    if limite is not None:
        sql += " LIMIT ?"
        parametros = (limite,)

    return get_db().execute(sql, parametros).fetchall()


def buscar_movimentacao(movimentacao_id):
    return get_db().execute(
        """
        SELECT
            movimentacoes.*,
            materiais.codigo AS material_codigo,
            materiais.nome AS material_nome,
            materiais.unidade_medida
        FROM movimentacoes
        INNER JOIN materiais
            ON materiais.id = movimentacoes.material_id
        WHERE movimentacoes.id = ?
        """,
        (movimentacao_id,),
    ).fetchone()


def registrar_movimentacao(
    material_id,
    tipo,
    quantidade,
    data_movimentacao,
    responsavel,
    destino="",
    observacao="",
):
    db = get_db()
    material = buscar_material(material_id)

    if material is None:
        raise ValueError("Material não encontrado.")

    if tipo not in ("entrada", "saida"):
        raise ValueError("Tipo de movimentação inválido.")

    quantidade = float(quantidade)

    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    if not data_movimentacao:
        raise ValueError("A data da movimentação é obrigatória.")

    if not str(responsavel).strip():
        raise ValueError("O responsável é obrigatório.")

    try:
        if tipo == "entrada":
            db.execute(
                """
                UPDATE materiais
                SET quantidade = quantidade + ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (quantidade, material_id),
            )
        else:
            cursor = db.execute(
                """
                UPDATE materiais
                SET quantidade = quantidade - ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND quantidade >= ?
                """,
                (quantidade, material_id, quantidade),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    "Estoque insuficiente para esta saída."
                )

        cursor = db.execute(
            """
            INSERT INTO movimentacoes (
                material_id,
                tipo,
                quantidade,
                data_movimentacao,
                responsavel,
                destino,
                observacao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                material_id,
                tipo,
                quantidade,
                data_movimentacao,
                str(responsavel).strip(),
                str(destino).strip(),
                str(observacao).strip(),
            ),
        )

        db.commit()
        return cursor.lastrowid

    except Exception:
        db.rollback()
        raise
