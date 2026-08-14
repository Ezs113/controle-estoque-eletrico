from database import get_db


MATERIAIS_EXEMPLO = [
    (
        "MAT-001",
        "Cabo flexível 1,5 mm² (Azul)",
        "Condutores",
        "Metros",
        420,
        100,
        "Prateleira A1",
    ),
    (
        "MAT-002",
        "Cabo flexível 2,5 mm² (Vermelho)",
        "Condutores",
        "Metros",
        350,
        100,
        "Prateleira A2",
    ),
    (
        "MAT-003",
        "Cabo flexível 4 mm² (Preto)",
        "Condutores",
        "Metros",
        180,
        80,
        "Prateleira A3",
    ),
    (
        "MAT-004",
        "Cabo flexível 6 mm² (Verde)",
        "Condutores",
        "Metros",
        95,
        50,
        "Prateleira A4",
    ),
    (
        "MAT-005",
        "Cabo PP 3x2,5 mm²",
        "Condutores",
        "Metros",
        120,
        40,
        "Prateleira A5",
    ),
    (
        "MAT-006",
        "Disjuntor monopolar 10A",
        "Proteção",
        "Unidades",
        28,
        10,
        "Prateleira B1",
    ),
    (
        "MAT-007",
        "Disjuntor monopolar 20A",
        "Proteção",
        "Unidades",
        32,
        10,
        "Prateleira B2",
    ),
    (
        "MAT-008",
        "Disjuntor bipolar 20A",
        "Proteção",
        "Unidades",
        8,
        10,
        "Prateleira B3",
    ),
    (
        "MAT-009",
        "Disjuntor tripolar 32A",
        "Proteção",
        "Unidades",
        12,
        5,
        "Prateleira B4",
    ),
    (
        "MAT-010",
        "Fusível NH 100A",
        "Proteção",
        "Unidades",
        6,
        8,
        "Prateleira B5",
    ),
    (
        "MAT-011",
        "Tomada 10A 2P+T",
        "Tomadas e Interruptores",
        "Unidades",
        45,
        15,
        "Prateleira C1",
    ),
    (
        "MAT-012",
        "Tomada 20A 2P+T",
        "Tomadas e Interruptores",
        "Unidades",
        30,
        10,
        "Prateleira C2",
    ),
    (
        "MAT-013",
        "Interruptor simples 1 tecla",
        "Tomadas e Interruptores",
        "Unidades",
        6,
        10,
        "Prateleira C3",
    ),
    (
        "MAT-014",
        "Interruptor paralelo 1 tecla",
        "Tomadas e Interruptores",
        "Unidades",
        18,
        8,
        "Prateleira C4",
    ),
    (
        "MAT-015",
        "Plugue industrial 32A",
        "Tomadas e Interruptores",
        "Unidades",
        9,
        4,
        "Prateleira C5",
    ),
    (
        "MAT-016",
        "Eletroduto PVC 3/4\"",
        "Tubulações",
        "Barras",
        72,
        20,
        "Área D1",
    ),
    (
        "MAT-017",
        "Eletroduto galvanizado 1\"",
        "Tubulações",
        "Barras",
        36,
        12,
        "Área D2",
    ),
    (
        "MAT-018",
        "Canaleta elétrica 30x30",
        "Tubulações",
        "Barras",
        24,
        8,
        "Área D3",
    ),
    (
        "MAT-019",
        "Curva PVC 90° 3/4\"",
        "Tubulações",
        "Unidades",
        55,
        20,
        "Prateleira D4",
    ),
    (
        "MAT-020",
        "Caixa de passagem 4x4",
        "Tubulações",
        "Unidades",
        38,
        12,
        "Prateleira D5",
    ),
    (
        "MAT-021",
        "Lâmpada LED tubular 18W",
        "Iluminação",
        "Unidades",
        40,
        12,
        "Prateleira E1",
    ),
    (
        "MAT-022",
        "Lâmpada LED bulbo 12W",
        "Iluminação",
        "Unidades",
        60,
        15,
        "Prateleira E2",
    ),
    (
        "MAT-023",
        "Refletor LED 100W",
        "Iluminação",
        "Unidades",
        7,
        5,
        "Prateleira E3",
    ),
    (
        "MAT-024",
        "Contator tripolar 25A",
        "Comando e Automação",
        "Unidades",
        4,
        5,
        "Prateleira F1",
    ),
    (
        "MAT-025",
        "Relé térmico 7-10A",
        "Comando e Automação",
        "Unidades",
        9,
        4,
        "Prateleira F2",
    ),
    (
        "MAT-026",
        "Relé auxiliar 24VCC",
        "Comando e Automação",
        "Unidades",
        16,
        6,
        "Prateleira F3",
    ),
    (
        "MAT-027",
        "Botão de emergência",
        "Comando e Automação",
        "Unidades",
        11,
        4,
        "Prateleira F4",
    ),
    (
        "MAT-028",
        "Terminal tubular 2,5 mm²",
        "Conexões",
        "Caixas",
        18,
        6,
        "Prateleira G1",
    ),
    (
        "MAT-029",
        "Conector de emenda 3 vias",
        "Conexões",
        "Caixas",
        14,
        5,
        "Prateleira G2",
    ),
    (
        "MAT-030",
        "Borne de passagem 4 mm²",
        "Conexões",
        "Unidades",
        75,
        20,
        "Prateleira G3",
    ),
]


MOVIMENTACOES_EXEMPLO = [
    (
        "MAT-002",
        "entrada",
        200,
        "2026-08-07",
        "Carlos Silva",
        "",
        "Compra Nota Fiscal 4589",
    ),
    (
        "MAT-008",
        "saida",
        5,
        "2026-08-07",
        "João Souza",
        "Manutenção no Bloco B",
        "Substituição de disjuntores",
    ),
    (
        "MAT-011",
        "saida",
        12,
        "2026-08-06",
        "Marcos Lima",
        "Laboratório 3",
        "Reforma do laboratório",
    ),
    (
        "MAT-016",
        "entrada",
        50,
        "2026-08-06",
        "Carlos Silva",
        "",
        "Reposição semanal de estoque",
    ),
    (
        "MAT-013",
        "saida",
        8,
        "2026-08-05",
        "Lucas Mendes",
        "Sala dos Professores",
        "Instalação de interruptores",
    ),
    (
        "MAT-021",
        "entrada",
        30,
        "2026-08-04",
        "Ana Ferreira",
        "",
        "Aquisição para manutenção preventiva",
    ),
    (
        "MAT-024",
        "saida",
        2,
        "2026-08-03",
        "João Souza",
        "Painel elétrico do Bloco A",
        "Substituição de contator",
    ),
    (
        "MAT-028",
        "entrada",
        10,
        "2026-08-02",
        "Ana Ferreira",
        "",
        "Reposição de terminais",
    ),
    (
        "MAT-023",
        "saida",
        2,
        "2026-08-01",
        "Marcos Lima",
        "Estacionamento",
        "Manutenção da iluminação externa",
    ),
    (
        "MAT-030",
        "entrada",
        50,
        "2026-08-01",
        "Carlos Silva",
        "",
        "Compra para montagem de painéis",
    ),
]


def seed_db():
    db = get_db()

    total_materiais = db.execute(
        "SELECT COUNT(*) FROM materiais"
    ).fetchone()[0]

    if total_materiais > 0:
        raise ValueError(
            "O banco já possui materiais cadastrados."
        )

    try:
        db.executemany(
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
            MATERIAIS_EXEMPLO,
        )

        materiais_por_codigo = {
            material["codigo"]: material["id"]
            for material in db.execute(
                "SELECT id, codigo FROM materiais"
            ).fetchall()
        }

        movimentacoes = [
            (
                materiais_por_codigo[codigo],
                tipo,
                quantidade,
                data_movimentacao,
                responsavel,
                destino,
                observacao,
            )
            for (
                codigo,
                tipo,
                quantidade,
                data_movimentacao,
                responsavel,
                destino,
                observacao,
            ) in MOVIMENTACOES_EXEMPLO
        ]

        db.executemany(
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
            movimentacoes,
        )

        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "materiais": len(MATERIAIS_EXEMPLO),
        "movimentacoes": len(MOVIMENTACOES_EXEMPLO),
    }
