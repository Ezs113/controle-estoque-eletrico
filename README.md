# Controle de Estoque de Materiais Elétricos

Trabalho Final — Pós-Graduação UTFPR

Sistema de controle de estoque de materiais elétricos desenvolvido para gestão de almoxarifado, controle de entradas, saídas, consulta de saldos em estoque e histórico de movimentações.

## Integrantes do Projeto

- **Adriano Lopes** — Backend
- **Ezequiel Souza** — Frontend

## Tecnologias Previstas

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Git
- GitHub

> **Situação do Projeto**: O frontend da aplicação encontra-se totalmente desenvolvido e funcional. A estrutura base do backend está devidamente preparada, e a implementação com Flask e SQLite será realizada posteriormente.

## Estrutura do Projeto

```text
controle-estoque-eletrico/
│
├── app.py                      # Aplicação Flask (preparado)
├── config.py                   # Configurações do projeto (preparado)
├── database.py                 # Conexão com o banco de dados (preparado)
├── README.md                   # Documentação do projeto
├── .gitignore                  # Arquivo de exclusão do Git
│
├── banco/
│   └── estoque.db              # Banco de dados SQLite (preparado)
│
├── models/
│   └── __init__.py             # Modelos de dados (preparado)
│
├── routes/
│   └── __init__.py             # Rotas da aplicação (preparado)
│
├── static/
│   ├── css/
│   │   └── style.css           # Estilos personalizados
│   ├── js/
│   │   └── main.js             # Scripts e filtros da interface
│   └── img/
│       └── .gitkeep            # Diretório de imagens
│
└── templates/
    ├── index.html              # Dashboard
    ├── materiais.html          # Cadastro de materiais
    ├── entrada.html            # Entrada de estoque
    ├── saida.html              # Saída de estoque
    ├── estoque.html            # Consulta de estoque
    └── historico.html          # Histórico de movimentações
```
