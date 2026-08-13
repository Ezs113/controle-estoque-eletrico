# API do Controle de Estoque

Documentação para integração do frontend com o backend Flask.

## Configuração

- Formato das requisições: JSON
- Cabeçalho: `Content-Type: application/json`
- Endereço de teste: `http://192.168.1.106:5000`

## Materiais

### Listar materiais

```http
GET /api/materiais
```

### Consultar material

```http
GET /api/materiais/{id}
```

### Cadastrar material

```http
POST /api/materiais
```

Corpo:

```json
{
  "codigo": "MAT-007",
  "nome": "Lâmpada LED Tubular 18W",
  "categoria": "Iluminação",
  "unidade_medida": "Unidades",
  "quantidade": 20,
  "estoque_minimo": 5,
  "localizacao": "Prateleira B1"
}
```

### Atualizar material

```http
PUT /api/materiais/{id}
```

Utiliza os mesmos campos do cadastro.

### Excluir material

```http
DELETE /api/materiais/{id}
```

Materiais que possuem movimentações não podem ser excluídos.

## Movimentações

### Registrar entrada

```http
POST /api/movimentacoes/entrada
```

```json
{
  "material_id": 1,
  "quantidade": 200,
  "data_movimentacao": "2026-08-07",
  "responsavel": "Carlos Silva",
  "observacao": "Compra Nota Fiscal 4589"
}
```

### Registrar saída

```http
POST /api/movimentacoes/saida
```

```json
{
  "material_id": 1,
  "quantidade": 5,
  "data_movimentacao": "2026-08-07",
  "responsavel": "João Souza",
  "destino": "Manutenção Elétrica do Bloco B",
  "observacao": "Troca de disjuntores"
}
```

A API impede saídas com quantidade superior ao estoque disponível.

### Listar movimentações

```http
GET /api/movimentacoes
```

Filtros opcionais:

| Parâmetro | Valores |
|---|---|
| `busca` | Texto livre |
| `tipo` | `todos`, `entrada` ou `saida` |
| `data_inicio` | Data no formato `AAAA-MM-DD` |
| `data_fim` | Data no formato `AAAA-MM-DD` |

Exemplo:

```http
GET /api/movimentacoes?tipo=saida&data_inicio=2026-08-01&data_fim=2026-08-31&busca=bloco
```

### Consultar movimentação

```http
GET /api/movimentacoes/{id}
```

## Dashboard

```http
GET /api/dashboard
```

Resposta:

```json
{
  "indicadores": {
    "materiais_cadastrados": 48,
    "total_itens": 1250,
    "estoque_baixo": 3,
    "entradas_mes": 14,
    "saidas_mes": 22
  },
  "movimentacoes_recentes": []
}
```

## Códigos HTTP

| Código | Significado |
|---|---|
| `200` | Operação realizada |
| `201` | Registro criado |
| `400` | Dados inválidos |
| `404` | Registro não encontrado |
| `409` | Conflito com dados existentes |

Os erros são retornados assim:

```json
{
  "erro": "Descrição do erro."
}
```

## Exemplo JavaScript

```javascript
async function carregarMateriais() {
    const resposta = await fetch("/api/materiais");
    const dados = await resposta.json();

    if (!resposta.ok) {
        throw new Error(dados.erro);
    }

    return dados;
}
```

## Executar o backend

```bash
source .venv/bin/activate
pip install -r requirements.txt
python -m flask --app app init-db
python -m flask --app app run --debug --host=0.0.0.0 --port=5000
```
