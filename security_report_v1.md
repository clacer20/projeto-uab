# Relatório de Inspeção de Segurança - v1.0

Este relatório detalha as vulnerabilidades de cibersegurança identificadas no **Sistema de Microblog**, com base no OWASP Top 10 e nas melhores práticas de desenvolvimento seguro.

## 1. Resumo Executivo

| Severidade | Quantidade |
| :--- | :--- |
| 🔴 Crítica | 2 |
| 🟠 Alta | 4 |
| 🟡 Média | 3 |
| 🔵 Baixa | 1 |
| **Total** | **10** |

### As 5 Ações Mais Urgentes
1. **Desativar o Modo Debug:** O modo debug permite execução remota de código (RCE).
2. **Implementar Autenticação:** Qualquer pessoa pode editar ou deletar dados.
3. **Proteção CSRF:** Adicionar tokens CSRF para evitar ações maliciosas em nome do usuário.
4. **Isolamento de Privilégios (Docker):** Impedir que a aplicação rode como root.
5. **Sanitização de Entrada:** Prevenir ataques de XSS e injeção de conteúdo.

---

## 2. Detalhamento de Vulnerabilidades

### V01: Modo Debug Ativado em Produção
- **Localização:** `run.py`, linha 4, função `__main__`.
- **Descrição:** A aplicação está configurada para rodar com `debug=True`, o que ativa o debugger interativo do Flask.
- **Evidência:** `app.run(host="0.0.0.0", port=5000, debug=True)`
- **Impacto:** Permite que um atacante execute código arbitrário (RCE) no servidor através do console interativo exposto em caso de erro.
- **Severidade:** 🔴 Crítica
- **Recomendação:** Alterar para `debug=False` ou usar variável de ambiente.
  ```python
  app.run(host="127.0.0.1", port=5000, debug=False)
  ```
- **Referências:** CWE-489 (Active Debug Code), OWASP A02:2021.

### V02: Ausência Total de Autenticação e Autorização
- **Localização:** `app/routes.py`, em todas as rotas (`nova_postagem`, `editar_postagem`, `deletar_postagem`, `relatorios`).
- **Descrição:** Não há verificação de identidade ou permissões. Qualquer usuário com acesso à URL pode alterar dados.
- **Evidência:** Ausência de decoradores `@login_required` ou lógica de verificação de usuário.
- **Impacto:** Manipulação não autorizada de dados, deleção de conteúdo e acesso a relatórios gerenciais por terceiros.
- **Severidade:** 🔴 Crítica
- **Recomendação:** Implementar `Flask-Login` ou similar e proteger as rotas.
- **Referências:** CWE-284 (Improper Access Control), OWASP A01:2021.

### V03: Ausência de Proteção contra CSRF
- **Localização:** `app/routes.py` (métodos POST) e `app/templates/index.html` (formulário de deleção).
- **Descrição:** A aplicação não utiliza tokens CSRF para validar requisições de mudança de estado.
- **Evidência:** `<form action="{{ url_for('deletar_postagem', id=post.id) }}" method="POST">` sem token oculto.
- **Impacto:** Um atacante pode induzir um usuário autenticado a deletar ou criar postagens via sites maliciosos.
- **Severidade:** 🟠 Alta
- **Recomendação:** Utilizar `Flask-WTF` e adicionar `{{ form.csrf_token }}` nos templates.
- **Referências:** CWE-352 (CSRF), OWASP A01:2021.

### V04: Execução como Root no Container Docker
- **Localização:** `Dockerfile`.
- **Descrição:** O container executa processos com o usuário root por padrão.
- **Evidência:** Ausência da instrução `USER` no `Dockerfile`.
- **Impacto:** Facilita ataques de "container breakout", dando ao atacante privilégios de root no host caso o container seja comprometido.
- **Severidade:** 🟠 Alta
- **Recomendação:** Criar um usuário não-privilegiado.
  ```dockerfile
  RUN useradd -m myuser
  USER myuser
  ```
- **Referências:** CWE-250 (Execution with Unnecessary Privileges), OWASP A02:2021.

### V05: Fallback de Chave Secreta Inseguro
- **Localização:** `app/__init__.py`, linha 12.
- **Descrição:** A `SECRET_KEY` utiliza um valor padrão caso a variável de ambiente não esteja definida.
- **Evidência:** `app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-key')`
- **Impacto:** Facilita ataques de falsificação de sessão e tokens se a chave padrão for usada.
- **Severidade:** 🟠 Alta
- **Recomendação:** Remover o fallback e garantir que a aplicação não inicie sem uma chave real.
- **Referências:** CWE-337 (Predictable Seed in PRNG), OWASP A02:2021.

### V06: Falta de Sanitização de Entrada (Risco de XSS)
- **Localização:** `app/utils.py`, função `validar_postagem`.
- **Descrição:** A validação apenas remove espaços em branco, sem filtrar tags HTML ou caracteres perigosos.
- **Evidência:** `t = titulo.strip() if titulo else ""`
- **Impacto:** Injeção de scripts maliciosos (Stored XSS) que podem roubar cookies de outros usuários.
- **Severidade:** 🟠 Alta
- **Recomendação:** Utilizar bibliotecas como `bleach` para limpar o HTML antes de salvar no banco.
- **Referências:** CWE-79 (XSS), OWASP A03:2021.

### V07: Exposição de Interface de Rede (0.0.0.0)
- **Localização:** `run.py`, linha 4.
- **Descrição:** A aplicação escuta em todas as interfaces de rede disponíveis.
- **Evidência:** `app.run(host="0.0.0.0", ...)`
- **Impacto:** Aumenta a superfície de ataque ao permitir conexões diretas de qualquer rede acessível ao servidor.
- **Severidade:** 🟡 Média
- **Recomendação:** Alterar para `127.0.0.1` e usar um proxy reverso (Nginx) para acesso externo.
- **Referências:** CWE-668 (Exposure of Resource to Wrong Sphere).

### V08: Processamento em Segundo Plano sem Limites
- **Localização:** `app/jobs.py`, função `background_process_post`.
- **Descrição:** Cada postagem cria uma nova thread sem controle de pool ou fila.
- **Evidência:** `thread = threading.Thread(target=task); thread.start()`
- **Impacto:** Risco de Negação de Serviço (DoS) por exaustão de recursos do sistema (fork bomb/thread exhaustion).
- **Severidade:** 🟡 Média
- **Recomendação:** Usar uma fila de tarefas (Celery/Redis) ou um `ThreadPoolExecutor` limitado.
- **Referências:** CWE-400 (Uncontrolled Resource Consumption).

### V09: Dependências sem Versões Fixas
- **Localização:** `requirements.txt`.
- **Descrição:** Os pacotes necessários não possuem versões travadas.
- **Evidência:** `Flask`, `Flask-SQLAlchemy` (sem `==version`).
- **Impacto:** Introdução involuntária de bugs ou vulnerabilidades em atualizações automáticas de pacotes.
- **Severidade:** 🟡 Média
- **Recomendação:** Utilizar `pip freeze > requirements.txt` para travar as versões.
- **Referências:** OWASP A06:2021.

### V10: Uso de SQLite em Produção
- **Localização:** `app/__init__.py`.
- **Descrição:** A aplicação utiliza um arquivo local SQLite para persistência em um ambiente containerizado.
- **Evidência:** `app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"`
- **Impacto:** Problemas de concorrência e integridade de dados em acessos simultâneos, além de perda de dados se o volume não for gerenciado corretamente.
- **Severidade:** 🔵 Baixa
- **Recomendação:** Migrar para PostgreSQL ou MySQL para ambientes de produção.
- **Referências:** CWE-1065 (Runtime Database System Selection).
