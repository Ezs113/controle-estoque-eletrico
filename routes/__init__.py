import sqlite3
from datetime import date

from flask import Blueprint, jsonify, request

from models import (
    atualizar_material,
    buscar_material,
    buscar_material_por_codigo,
    buscar_movimentacao,
    criar_material,
    excluir_material,
    listar_materiais,
    listar_movimentacoes,
    registrar_movimentacao,
)


api = Blueprint("api", __name__, url_prefix="/api")


def registro_para_dict(registro):
    return dict(registro)


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
        return (
            "Campos obrigatórios ausentes: "
            + ", ".join(campos_ausentes)
        )

    try:
        quantidade = float(dados["quantidade"])
        estoque_minimo = float(dados["estoque_minimo"])
    except (TypeError, ValueError):
        return "Quantidade e estoque mínimo devem ser números."

    if quantidade < 0 or estoque_minimo < 0:
        return (
            "Quantidade e estoque mínimo não podem ser negativos."
        )

    return None


def validar_movimentacao(dados):
    campos_obrigatorios = (
        "material_id",
        "quantidade",
        "data_movimentacao",
        "responsavel",
    )

    campos_ausentes = [
        campo
        for campo in campos_obrigatorios
        if campo not in dados or dados[campo] in (None, "")
    ]

    if campos_ausentes:
        return (
            "Campos obrigatórios ausentes: "
            + ", ".join(campos_ausentes)
        )

    try:
        material_id = int(dados["material_id"])
        quantidade = float(dados["quantidade"])
    except (TypeError, ValueError):
        return (
            "O material deve possuir um ID válido e a quantidade "
            "deve ser um número."
        )

    if material_id <= 0:
        return "O ID do material deve ser maior que zero."

    if quantidade <= 0:
        return "A quantidade deve ser maior que zero."

    try:
        date.fromisoformat(str(dados["data_movimentacao"]))
    except ValueError:
        return "A data deve estar no formato AAAA-MM-DD."

    if not str(dados["responsavel"]).strip():
        return "O responsável é obrigatório."

    return None


@api.get("/materiais")
def api_listar_materiais():
    materiais = listar_materiais()

    return jsonify(
        [registro_para_dict(material) for material in materiais]
    )


@api.get("/materiais/<int:material_id>")
def api_buscar_material(material_id):
    material = buscar_material(material_id)

    if material is None:
        return jsonify({"erro": "Material não encontrado."}), 404

    return jsonify(registro_para_dict(material))


@api.post("/materiais")
def api_criar_material():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify(
            {"erro": "Envie os dados no formato JSON."}
        ), 400

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
            unidade_medida=str(
                dados["unidade_medida"]
            ).strip(),
            quantidade=float(dados["quantidade"]),
            estoque_minimo=float(dados["estoque_minimo"]),
            localizacao=str(
                dados.get("localizacao", "")
            ).strip(),
        )
    except sqlite3.IntegrityError:
        return jsonify(
            {"erro": "Não foi possível cadastrar o material."}
        ), 409

    material = buscar_material(material_id)

    return jsonify(
        {
            "mensagem": "Material cadastrado com sucesso.",
            "material": registro_para_dict(material),
        }
    ), 201


@api.put("/materiais/<int:material_id>")
def api_atualizar_material(material_id):
    material = buscar_material(material_id)

    if material is None:
        return jsonify({"erro": "Material não encontrado."}), 404

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify(
            {"erro": "Envie os dados no formato JSON."}
        ), 400

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
            unidade_medida=str(
                dados["unidade_medida"]
            ).strip(),
            quantidade=float(dados["quantidade"]),
            estoque_minimo=float(dados["estoque_minimo"]),
            localizacao=str(
                dados.get("localizacao", "")
            ).strip(),
        )
    except sqlite3.IntegrityError:
        return jsonify(
            {"erro": "Não foi possível atualizar o material."}
        ), 409

    return jsonify(
        {
            "mensagem": "Material atualizado com sucesso.",
            "material": registro_para_dict(
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
                    "O material possui movimentações e não pode "
                    "ser excluído."
                )
            }
        ), 409

    return jsonify(
        {"mensagem": "Material excluído com sucesso."}
    )


@api.get("/movimentacoes")
def api_listar_movimentacoes():
    movimentacoes = listar_movimentacoes()

    return jsonify(
        [
            registro_para_dict(movimentacao)
            for movimentacao in movimentacoes
        ]
    )


@api.get("/movimentacoes/<int:movimentacao_id>")
def api_buscar_movimentacao(movimentacao_id):
    movimentacao = buscar_movimentacao(movimentacao_id)

    if movimentacao is None:
        return jsonify(
            {"erro": "Movimentação não encontrada."}
        ), 404

    return jsonify(registro_para_dict(movimentacao))


def criar_movimentacao_por_tipo(tipo):
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify(
            {"erro": "Envie os dados no formato JSON."}
        ), 400

    erro = validar_movimentacao(dados)

    if erro:
        return jsonify({"erro": erro}), 400

    try:
        movimentacao_id = registrar_movimentacao(
            material_id=int(dados["material_id"]),
            tipo=tipo,
            quantidade=float(dados["quantidade"]),
            data_movimentacao=str(
                dados["data_movimentacao"]
            ),
            responsavel=str(dados["responsavel"]),
            destino=str(dados.get("destino", "")),
            observacao=str(dados.get("observacao", "")),
        )
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    except sqlite3.IntegrityError:
        return jsonify(
            {"erro": "Não foi possível registrar a movimentação."}
        ), 409

    movimentacao = buscar_movimentacao(movimentacao_id)

    return jsonify(
        {
            "mensagem": (
                f"{tipo.capitalize()} registrada com sucesso."
            ),
            "movimentacao": registro_para_dict(movimentacao),
            "material": registro_para_dict(
                buscar_material(int(dados["material_id"]))
            ),
        }
    ), 201


@api.post("/movimentacoes/entrada")
def api_registrar_entrada():
    return criar_movimentacao_por_tipo("entrada")


@api.post("/movimentacoes/saida")
def api_registrar_saida():
    return criar_movimentacao_por_tipo("saida")
