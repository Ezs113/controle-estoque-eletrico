# Controle de Estoque de Materiais Elétricos

Trabalho Final — Pós-Graduação UTFPR

Sistema de Controle de Estoque de Materiais Elétricos desenvolvido como projeto acadêmico para gestão de almoxarifado, acompanhamento de entradas e saídas, consulta de saldos em estoque e histórico de movimentações.

## Integrantes do Projeto

- Adriano Lopes — Backend
- Ezequiel Souza — Frontend

## Tecnologias Utilizadas

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Git
- GitHub

## Estado Atual do Sistema

O sistema encontra-se totalmente integrado e funcional, com o frontend consumindo os endpoints da API Flask e com suporte a persistência de dados no banco de dados SQLite.

## Funcionalidades Implementadas

- Dashboard com indicadores gerais do estoque e movimentações recentes
- Cadastro, consulta, edição e exclusão (CRUD) de materiais elétricos
- Registro de entradas de estoque com atualização de saldos
- Registro de saídas de estoque com validação de quantidades disponíveis
- Consulta de situação do estoque (com identificação de estoque baixo e zerado)
- Histórico completo de movimentações com filtros por texto, tipo e período de datas
- Integração dinâmica frontend/backend por meio de API REST
- Persistência e integridade referencial dos dados em banco SQLite

## Estrutura do Projeto

```text
controle-estoque-eletrico/
│
├── app.py                      # Arquivo principal da aplicação Flask e rotas de templates
├── config.py                   # Configurações globais e caminho do banco de dados
├── database.py                 # Funções de conexão e inicialização do banco SQLite
├── seed.py                     # Script para inserção de dados iniciais no banco
├── requirements.txt            # Dependências Python do projeto
├── API.md                      # Documentação das rotas e especificações da API REST
├── README.md                   # Documentação do projeto
├── .gitignore                  # Regras de exclusão do Git
│
├── banco/
│   └── estoque.db              # Banco de dados SQLite da aplicação
│
├── models/
│   └── __init__.py             # Funções de manipulação de dados e consultas SQL
│
├── routes/
│   └── __init__.py             # Definição dos endpoints REST da API
│
├── static/
│   ├── css/
│   │   └── style.css           # Estilos personalizados do sistema
│   ├── js/
│   │   └── main.js             # Lógica e chamadas AJAX (fetch API) no frontend
│   └── img/
│       └── .gitkeep            # Diretório de armazenamento de imagens
│
└── templates/                  # Interfaces HTML do sistema
    ├── index.html              # Dashboard principal
    ├── materiais.html          # Cadastro e gestão de materiais
    ├── entrada.html            # Formulário de entrada de estoque
    ├── saida.html              # Formulário de saída de estoque
    ├── estoque.html            # Consulta e situação do estoque
    └── historico.html          # Histórico geral de movimentações
```

## Como Executar o Projeto Localmente

### 1. Acessar o Diretório do Projeto

No terminal ou prompt de comando, navegue até a pasta do projeto:

```bash
cd C:\UTFPR\Projetos\controle-estoque-eletrico
```

### 2. Criar e Ativar o Ambiente Virtual

Criar o ambiente virtual Python:

```bash
python -m venv .venv
```

Ativar o ambiente virtual:

- **No Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

- **No Windows (Prompt de Comando - CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

- **No Linux ou macOS:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Instalar as Dependências

Com o ambiente virtual ativado, instale as dependências contidas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Inicializar o Banco de Dados (Opcional / Carga Inicial)

Caso necessite popular o banco de dados com a estrutura e os dados iniciais de teste:

```bash
python seed.py
```

### 5. Executar o Servidor Flask

Inicie a aplicação:

```bash
python app.py
```

Acesse a aplicação no navegador por meio do endereço:
`http://127.0.0.1:5000`
