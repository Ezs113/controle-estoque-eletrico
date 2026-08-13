import sqlite3

from flask import Blueprint, jsonify, request

from models import (
    atualizar_material,
    buscar_material,
    buscar_material_por_codigo,
    criar_material,
    excluir_material,
    listar_materiais,
)


api = Blueprint("api", __name__, url_prefix="/api")


def material_para_dict(material):
    return dict(material)


def validar_material(dados):
    campos_obrigatorios = (
        "codigo",
        "nome",
        "categoria",
        "unidade_medida",
        "quantidade",
        "estoque_minimo",
    )

    campos_ausentes = [
        campo
        for campo in campos_obrigatorios
        if campo not in dados or dados[campo] in (None, "")
    ]

    if campos_ausentes:
        return f"Campos obrigatórios ausentes: {', '.join(campos_ausentes)}"

    try:
        quantidade = float(dados["quantidade"])
        estoque_minimo = float(dados["estoque_minimo"])
    except (TypeError, ValueError):
        return "Quantidade e estoque mínimo devem ser números."

    if quantidade < 0 or estoque_minimo < 0:
        return "Quantidade e estoque mínimo não podem ser negativos."

    return None


@api.get("/materiais")
def api_listar_materiais():
    materiais = listar_materiais()

    return jsonify(
        [material_para_dict(material) for material in materiais]
    )


@api.get("/materiais/<int:material_id>")
def api_buscar_material(material_id):
    material = buscar_material(material_id)

    if material is None:
        return jsonify({"erro": "Material não encontrado."}), 404

    return jsonify(material_para_dict(material))


@api.post("/materiais")
def api_criar_material():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie os dados no formato JSON."}), 400

    erro = validar_material(dados)

    if erro:
        return jsonify({"erro": erro}), 400

    codigo = str(dados["codigo"]).strip()
    nome = str(dados["nome"]).strip()

    if not codigo or not nome:
        return jsonify(
            {"erro": "Código e nome não podem ficar vazios."}
        ), 400

    if buscar_material_por_codigo(codigo) is not None:
        return jsonify(
            {"erro": "Já existe um material com esse código."}
        ), 409

    try:
        material_id = criar_material(
            codigo=codigo,
            nome=nome,
            categoria=str(dados["categoria"]).strip(),
            unidade_medida=str(dados["unidade_medida"]).strip(),
            quantidade=float(dados["quantidade"]),
            estoque_minimo=float(dados["estoque_minimo"]),
            localizacao=str(dados.get("localizacao", "")).strip(),
        )
    except sqlite3.IntegrityError:
        return jsonify(
            {"erro": "Não foi possível cadastrar o material."}
        ), 409

    material = buscar_material(material_id)

    return jsonify(
        {
            "mensagem": "Material cadastrado com sucesso.",
            "material": material_para_dict(material),
        }
    ), 201


@api.put("/materiais/<int:material_id>")
def api_atualizar_material(material_id):
    material = buscar_material(material_id)

    if material is None:
        return jsonify({"erro": "Material não encontrado."}), 404

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie os dados no formato JSON."}), 400

    erro = validar_material(dados)

    if erro:
        return jsonify({"erro": erro}), 400

    codigo = str(dados["codigo"]).strip()
    nome = str(dados["nome"]).strip()
    material_mesmo_codigo = buscar_material_por_codigo(codigo)

    if not codigo or not nome:
        return jsonify(
            {"erro": "Código e nome não podem ficar vazios."}
        ), 400

    if (
        material_mesmo_codigo is not None
        and material_mesmo_codigo["id"] != material_id
    ):
        return jsonify(
            {"erro": "Já existe um material com esse código."}
        ), 409

    try:
        atualizar_material(
            material_id=material_id,
            codigo=codigo,
            nome=nome,
            categoria=str(dados["categoria"]).strip(),
            unidade_medida=str(dados["unidade_medida"]).strip(),
            quantidade=float(dados["quantidade"]),
            estoque_minimo=float(dados["estoque_minimo"]),
            localizacao=str(dados.get("localizacao", "")).strip(),
        )
    except sqlite3.IntegrityError:
        return jsonify(
            {"erro": "Não foi possível atualizar o material."}
        ), 409

    return jsonify(
        {
            "mensagem": "Material atualizado com sucesso.",
            "material": material_para_dict(
                buscar_material(material_id)
            ),
        }
    )


@api.delete("/materiais/<int:material_id>")
def api_excluir_material(material_id):
    material = buscar_material(material_id)

    if material is None:
        return jsonify({"erro": "Material não encontrado."}), 404

    try:
        excluir_material(material_id)
    except sqlite3.IntegrityError:
        return jsonify(
            {
                "erro": (
                    "O material possui movimentações e não pode ser excluído."
                )
            }
        ), 409

    return jsonify({"mensagem": "Material excluído com sucesso."})
