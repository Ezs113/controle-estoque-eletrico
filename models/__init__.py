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


def listar_movimentacoes(
    limite=None,
    busca=None,
    tipo=None,
    data_inicio=None,
    data_fim=None,
):
    sql = """
        SELECT
            movimentacoes.*,
            materiais.codigo AS material_codigo,
            materiais.nome AS material_nome,
            materiais.unidade_medida
        FROM movimentacoes
        INNER JOIN materiais
            ON materiais.id = movimentacoes.material_id
        WHERE 1 = 1
    """

    parametros = []

    if busca:
        termo = f"%{busca.strip()}%"

        sql += """
            AND (
                materiais.codigo LIKE ?
                OR materiais.nome LIKE ?
                OR movimentacoes.responsavel LIKE ?
                OR movimentacoes.destino LIKE ?
                OR movimentacoes.observacao LIKE ?
            )
        """

        parametros.extend(
            (termo, termo, termo, termo, termo)
        )

    if tipo in ("entrada", "saida"):
        sql += " AND movimentacoes.tipo = ?"
        parametros.append(tipo)

    if data_inicio:
        sql += " AND movimentacoes.data_movimentacao >= ?"
        parametros.append(data_inicio)

    if data_fim:
        sql += " AND movimentacoes.data_movimentacao <= ?"
        parametros.append(data_fim)

    sql += """
        ORDER BY
            movimentacoes.data_movimentacao DESC,
            movimentacoes.id DESC
    """

    if limite is not None:
        sql += " LIMIT ?"
        parametros.append(limite)

    return get_db().execute(
        sql,
        tuple(parametros),
    ).fetchall()


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
        raise ValueError(
            "A data da movimentação é obrigatória."
        )

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


def obter_indicadores_dashboard():
    db = get_db()

    materiais = db.execute(
        """
        SELECT
            COUNT(*) AS materiais_cadastrados,
            COALESCE(SUM(quantidade), 0) AS total_itens,
            COALESCE(
                SUM(
                    CASE
                        WHEN quantidade <= estoque_minimo
                        THEN 1
                        ELSE 0
                    END
                ),
                0
            ) AS estoque_baixo
        FROM materiais
        """
    ).fetchone()

    movimentacoes_mes = db.execute(
        """
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN tipo = 'entrada'
                        THEN 1
                        ELSE 0
                    END
                ),
                0
            ) AS entradas_mes,
            COALESCE(
                SUM(
                    CASE
                        WHEN tipo = 'saida'
                        THEN 1
                        ELSE 0
                    END
                ),
                0
            ) AS saidas_mes
        FROM movimentacoes
        WHERE substr(data_movimentacao, 1, 7)
            = strftime('%Y-%m', 'now', 'localtime')
        """
    ).fetchone()

    return {
        "materiais_cadastrados": (
            materiais["materiais_cadastrados"]
        ),
        "total_itens": materiais["total_itens"],
        "estoque_baixo": materiais["estoque_baixo"],
        "entradas_mes": movimentacoes_mes["entradas_mes"],
        "saidas_mes": movimentacoes_mes["saidas_mes"],
    }


def obter_dashboard():
    return {
        "indicadores": obter_indicadores_dashboard(),
        "movimentacoes_recentes": [
            dict(movimentacao)
            for movimentacao in listar_movimentacoes(limite=5)
        ],
    }
