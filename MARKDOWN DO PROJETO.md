# Especificação Técnica - Sistema de Microblog

Este documento descreve a arquitetura, infraestrutura e lógica de implementação do Sistema de Microblog, refletindo o estado real e final do projeto.

## 1. Arquitetura e Infraestrutura

### Arquivos de Configuração
- **requirements.txt**: Define as dependências Python (Flask, Flask-SQLAlchemy, python-dotenv, pytest, pytest-mock).
- **Dockerfile**: Imagem base `python:3.10-slim`, configurada para rodar na porta 5000 via `run.py`.
- **docker-compose.yml**: Orquestra o serviço `web` e gerencia a persistência do banco SQLite via volume `sqlite_data` mapeado para `/app/instance`.
- **.env**: Gerencia variáveis sensíveis como `SECRET_KEY`.

### Ponto de Entrada (`run.py`)
Inicia o servidor Flask em `0.0.0.0:5000`. No ambiente de desenvolvimento, o `debug=True` está habilitado.

---

## 2. Implementação do Backend (App)

### Inicialização (`app/__init__.py`)
- Carrega variáveis de ambiente.
- Configura o banco de dados SQLite com caminhos absolutos para evitar erros de persistência.
- **Otimização de Performance (Cache):** Configuração do `Flask-Caching` com estratégia `SimpleCache` para otimizar rotas de leitura intensa.
- **Criação Automática:** Executa `db.create_all()` dentro do contexto da aplicação no startup, garantindo que as tabelas existam.

### Modelos (`app/models.py`)
- **Postagem**: Tabela com campos `id` (PK), `titulo` (String 100, Not Null) e `descricao` (Text, Not Null).

### Rotas e Lógica de Negócio (`app/routes.py`)
- **GET / (index)**: Lista todas as postagens em ordem decrescente de ID.
- **POST /postagens/nova**: 
  - Realiza sanitização e validação via helper `app.utils.validar_postagem`.
  - **Processamento Assíncrono (Jobs):** Dispara tarefa em segundo plano via `app.jobs.background_process_post` para processamento pós-criação.
  - Invalida o cache da página de relatórios.
- **POST /postagens/editar/<id>**:
  - Busca por ID ou 404.
  - Valida e atualiza campos.
  - Invalida o cache da página de relatórios.
- **POST /postagens/deletar/<id>**: 
  - Remove o registro permanentemente.
  - Invalida o cache da página de relatórios.
- **GET /relatorios**: 
  - **Cache:** Rota memorizada (`cache.memoize`) para reduzir acessos redundantes ao banco de dados em cálculos de métricas.

### Utilitários e Jobs
- **app/utils.py**: Centraliza a lógica de validação de dados para garantir o princípio DRY (Don't Repeat Yourself).
- **app/jobs.py**: Gerencia a execução de tarefas em segundo plano utilizando threads para não bloquear a resposta principal do servidor.
