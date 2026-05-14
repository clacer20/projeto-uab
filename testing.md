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
| T7 | Navegação | Cancelar Postagem | Crítica | Validar se o retorno da página de cadastro para a home (botão cancelar) ocorre sem erros de banco. |

## 3. Implementação dos Testes (TDD e Integração)

O projeto conta com dois conjuntos principais de testes:
1. **Testes de Unidade (`tests/test_app.py`):** Focam na lógica das rotas e comportamentos individuais do Flask.
2. **Testes de Integração (`tests/test_integration.py`):** Validam a comunicação entre Frontend (HTML/Templates), Backend (Lógica Flask) e Banco de Dados (Persistência Real).

### Detalhes dos Testes de Integração
- **test_full_flow_integration:** Realiza o fluxo completo — cria uma postagem via formulário web, verifica a gravação no banco de dados e confirma a exibição correta no feed inicial.
- **test_cancel_button_redirection:** Verifica especificamente a estabilidade do sistema ao navegar da página de criação de volta para a Home (simulando o botão Cancelar).
- **test_backend_logic_isolation:** Valida a integridade dos modelos e regras de negócio sem interface gráfica.
- **test_frontend_rendering_isolation:** Garante que os templates estão sendo renderizados com as variáveis corretas.

### Comando para Execução dentro do Docker (Recomendado)
Para executar todos os testes automatizados dentro do ambiente de contêiner:
```bash
docker exec microblog-web python3 -m pytest tests/test_app.py tests/test_integration.py
```

### Comando para Execução Local
Caso as dependências estejam instaladas localmente:
```bash
pytest
```

## 4. Mocks e Simulações
- **Banco de Dados:** Utilização de `:memory:` para isolamento total entre execuções de teste.
- **Contexto de App:** Uso de `pytest fixtures` para gerenciar o ciclo de vida da aplicação e do banco de dados durante os testes.
