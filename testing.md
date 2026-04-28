# Plano de Testes - Sistema de Microblog

Este documento descreve a estratégia de testes automatizados para o Sistema de Microblog, seguindo a metodologia **TDD (Test-Driven Development) First**. O objetivo é garantir a integridade das funcionalidades críticas e evitar regressões.

## 1. Estratégia de Testes

- **Abordagem:** Testes de Unidade e Integração utilizando `pytest`.
- **Ambiente:** Os testes utilizam uma instância do Flask configurada para modo de teste com um banco de dados SQLite em memória (`sqlite:///:memory:`).
- **Frequência:** Execução automatizada antes de cada commit/push.

## 2. Cenários de Teste por Funcionalidade

### 2.1. Gerenciamento de Postagens (CRUD)

| ID | Funcionalidade | Cenário | Prioridade | Descrição |
|:---|:---|:---|:---|:---|
| T1 | Criar Postagem | Sucesso | Crítica | Validar se uma postagem com título e descrição válidos é salva no banco. |
| T2 | Criar Postagem | Falha (Campos Vazios) | Alta | Garantir que o sistema não aceite postagens sem título ou sem descrição. |
| T3 | Editar Postagem | Sucesso | Crítica | Validar a atualização de conteúdo de uma postagem existente. |
| T4 | Deletar Postagem | Sucesso | Crítica | Garantir que a postagem seja removida permanentemente após a confirmação. |

### 2.2. Visualização e Relatórios

| ID | Funcionalidade | Cenário | Prioridade | Descrição |
|:---|:---|:---|:---|:---|
| T5 | Listagem (Index) | Ordem Decrescente | Média | Validar se as postagens são exibidas da mais recente para a mais antiga. |
| T6 | Relatórios | Cálculo de Total | Alta | Validar se o contador de postagens reflete o estado real do banco de dados. |

## 3. Implementação dos Testes (TDD)

Os testes devem simular o cliente HTTP do Flask (`app.test_client()`) para validar as rotas e o estado do banco de dados SQLAlchemy.

### Dependências para Execução
As dependências listadas no `requirements.txt` (incluindo `pytest`) devem ser instaladas:
```bash
pip install -r requirements.txt
```

### Comando para Execução
Para executar todos os testes:
```bash
pytest
```

## 4. Mocks e Simulações
- **Banco de Dados:** Utilização de `:memory:` para isolamento total entre execuções de teste.
- **Contexto de App:** Uso de `pytest fixtures` para gerenciar o ciclo de vida da aplicação e do banco de dados durante os testes.
