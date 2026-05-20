# Plano de Testes e Qualidade - Sistema de Microblog

Este documento reflete a estratégia de testes aplicada e os cenários cobertos para garantir a estabilidade do sistema.

## 1. Estratégia de Testes

- **Unidade e Integração:** Utiliza `pytest` com banco de dados em memória (`:memory:`) ou arquivo temporário para isolamento.
- **Ambiente:** Execução recomendada via Docker para garantir paridade com o ambiente de produção.

## 2. Cenários de Teste Cobertos

### 2.1. Backend e Lógica (CRUD)
- **T1 (Criação com Sucesso):** Valida se dados válidos são persistidos.
- **T2 (Falha de Validação):** Garante que campos vazios ou apenas com espaços retornam erro 400.
- **T3 (Edição):** Confirma a atualização correta de registros existentes.
- **T4 (Exclusão):** Verifica a remoção física do banco de dados.

### 2.2. Integração e UI
- **T5 (Ordenação):** Verifica se o feed exibe a postagem mais recente primeiro.
- **T6 (Métricas):** Valida se o contador na página de relatórios condiz com o banco.
- **T7 (Navegação):** Garante a estabilidade do fluxo de cancelamento de formulários.
- **F1 (Estado Vazio):** Verifica a renderização da mensagem amigável quando não há posts.
- **P1 (Cache):** Valida se a página de relatórios utiliza cache para performance, mas invalida corretamente após alterações no banco.
- **P2 (Jobs):** Verifica se o processamento pós-criação ocorre em segundo plano sem bloquear a resposta HTTP.

## 3. Comandos de Verificação

### Rodar todos os testes (Docker)
```bash
docker exec microblog-web python3 -m pytest tests/test_app.py tests/test_integration.py
```

### Rodar testes locais
```bash
pytest
```

## 4. Matriz de Qualidade (UX/A11y)
- **Responsividade:** Verificação manual de colapso da navbar e ajuste de cards.
- **Acessibilidade:** Uso de semântica HTML e foco por teclado em elementos interativos.
- **Fluxos de Erro:** Tratamento de 404 (ID inexistente) e 400 (Input inválido).
