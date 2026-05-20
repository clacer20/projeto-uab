# Relatório de Refatoração e Otimização

Este documento detalha as mudanças realizadas no Sistema de Microblog para simplificação, modularização e melhoria de desempenho.

## 1. Simplificação e Modularização
- **Helper de Validação:** Criado o arquivo `app/utils.py` com a função `validar_postagem`. Isso removeu a duplicidade de lógica de sanitização e validação de campos obrigatórios nas rotas de criação e edição.
- **Isolamento de Tarefas:** Criado o arquivo `app/jobs.py` para separar a lógica de processamento em segundo plano da lógica de controle de rotas.

## 2. Melhoria de Desempenho (Performance)
- **Implementação de Cache:**
  - Adicionada a biblioteca `Flask-Caching`.
  - Configurada a estratégia `SimpleCache` (em memória) no `app/__init__.py`.
  - Aplicado `cache.memoize` na rota `/relatorios` para evitar contagens redundantes no banco de dados SQLite.
  - Implementada a invalidação manual do cache (`cache.delete_memoized`) nas operações de escrita (Criar, Editar, Deletar) para garantir a consistência dos dados.
- **Processamento em Segundo Plano (Jobs/Filas):**
  - Implementada a execução de tarefas pós-criação de postagens utilizando `threading`. Isso permite que o servidor responda imediatamente ao usuário enquanto processos "pesados" (simulados) ocorrem em background.

## 3. Impacto e Estabilidade
- **Manutenção do CRUD:** Todas as operações básicas continuam funcionais e integradas com os novos componentes.
- **Isolamento de Falhas:** O uso de threads daemon garante que falhas em tarefas de background não derrubem o processo principal do servidor.
- **Validação:** A suíte de testes original e os novos cenários de performance foram validados com sucesso via Docker.

## 4. Dependências Atualizadas
- `Flask-Caching`: Necessária para a implementação da camada de performance.
