# Relatório Consolidado de Inspeção de Segurança - Sistema de Microblog

Este documento unifica todas as descobertas de segurança identificadas nas fases de auditoria e inspeção do **Sistema de Microblog**, consolidando informações sobre infraestrutura, código-fonte e configurações.

## 1. Resumo Executivo

| Severidade | Quantidade |
| :--- | :--- |
| 🔴 Crítica | 2 |
| 🟠 Alta | 4 |
| 🟡 Média | 3 |
| 🔵 Baixa | 1 |
| **Total** | **10** |

### As 5 Ações Mais Urgentes
1.  **Desativar o Modo Debug:** O modo debug permite execução remota de código (RCE) e exposição de dados sensíveis.
2.  **Implementar Autenticação:** Atualmente, qualquer usuário pode editar, deletar ou criar postagens sem permissão.
3.  **Habilitar Proteção CSRF:** Essencial para evitar que usuários realizem ações indesejadas via sites maliciosos.
4.  **Isolamento de Privilégios (Docker):** A aplicação não deve rodar como `root` no contêiner para prevenir ataques de escape.
5.  **Sanitização de Entradas (XSS):** Prevenir a execução de scripts maliciosos nos navegadores dos usuários.

---

## 2. Detalhamento de Vulnerabilidades

### V01: Modo Debug Ativado em Produção
- **Localização:** `run.py`, linha 4, função `__main__`.
- **Descrição:** A aplicação está configurada para rodar com `debug=True`, ativando o debugger interativo do Flask/Werkzeug.
- **Evidência:** 
  ```python
  if __name__ == '__main__':
      app.run(host="0.0.0.0", port=5000, debug=True)
  ```
- **Impacto:** Permite que um atacante execute código arbitrário (RCE) no servidor através do console interativo exposto em caso de erro, além de vazar variáveis de ambiente.
- **Severidade:** 🔴 Crítica
- **Recomendação:** Alterar para `debug=False` por padrão ou utilizar variáveis de ambiente para controle dinâmico.
- **Referências:** CWE-489 (Active Debug Code), OWASP A05:2021 (Security Misconfiguration).

### V02: Ausência Total de Autenticação e Autorização
- **Localização:** `app/routes.py`, em todas as rotas operacionais (`nova_postagem`, `editar_postagem`, `deletar_postagem`, `relatorios`).
- **Descrição:** Não existe qualquer barreira de acesso. O sistema não exige login nem verifica privilégios para operações críticas de CRUD.
- **Evidência:** Ausência de decoradores como `@login_required` ou lógica de validação de sessão nas rotas.
- **Impacto:** Destruição de dados (deleção em massa), modificação de conteúdo legítimo e acesso a dados gerenciais por pessoas não autorizadas.
- **Severidade:** 🔴 Crítica
- **Recomendação:** Implementar um sistema de identidade (ex: `Flask-Login`) e proteger as rotas com autenticação.
- **Referências:** CWE-284 (Improper Access Control), OWASP A01:2021 (Broken Access Control).

### V03: Ausência de Proteção contra CSRF (Cross-Site Request Forgery)
- **Localização:** `app/routes.py` (métodos POST) e `app/templates/index.html` (formulário de deleção).
- **Descrição:** Formulários que realizam mudanças de estado (POST) não utilizam tokens de segurança para validar a origem da requisição.
- **Evidência:** 
  ```html
  <form action="{{ url_for('deletar_postagem', id=post.id) }}" method="POST">
      <button type="submit" class="btn btn-sm btn-danger">Apagar</button>
  </form>
  ```
- **Impacto:** Um atacante pode criar uma página maliciosa que, ao ser visitada por um usuário logado, força o navegador a enviar uma requisição de deleção ou criação de postagem sem o conhecimento do usuário.
- **Severidade:** 🟠 Alta
- **Recomendação:** Utilizar a extensão `Flask-WTF` e incluir `{{ form.csrf_token }}` em todos os formulários.
- **Referências:** CWE-352 (CSRF), OWASP A01:2021 (Broken Access Control).

### V04: Execução como Root no Container Docker
- **Localização:** `Dockerfile`.
- **Descrição:** O processo da aplicação dentro do contêiner é executado com privilégios de root, pois nenhum usuário foi definido.
- **Evidência:** O arquivo `Dockerfile` termina com a execução direta do comando sem trocar o contexto de usuário.
- **Impacto:** Em caso de comprometimento da aplicação (via RCE, por exemplo), o invasor terá controle total sobre o contêiner e maior facilidade para realizar um "container breakout" para o host.
- **Severidade:** 🟠 Alta
- **Recomendação:** Adicionar um usuário de sistema e usar a instrução `USER`.
  ```dockerfile
  RUN useradd -m appuser
  USER appuser
  ```
- **Referências:** CWE-250 (Execution with Unnecessary Privileges), OWASP A05:2021 (Security Misconfiguration).

### V05: Fallback de Chave Secreta Inseguro
- **Localização:** `app/__init__.py`, linha 12.
- **Descrição:** A configuração da `SECRET_KEY` utiliza um valor padrão estático se a variável de ambiente não estiver definida.
- **Evidência:** 
  ```python
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-key')
  ```
- **Impacto:** Facilita ataques de decifração de sessões e tokens de segurança, permitindo o sequestro de contas se a chave padrão for mantida.
- **Severidade:** 🟠 Alta
- **Recomendação:** Forçar a falha da aplicação se a chave não estiver configurada no ambiente.
- **Referências:** CWE-337 (Predictable Seed in PRNG), OWASP A02:2021 (Cryptographic Failures).

### V06: Falta de Sanitização de Entrada (Risco de XSS)
- **Localização:** `app/utils.py`, função `validar_postagem`.
- **Descrição:** A validação de entrada apenas remove espaços, permitindo a inserção de tags `<script>` ou outros elementos HTML maliciosos.
- **Evidência:** 
  ```python
  t = titulo.strip() if titulo else ""
  d = descricao.strip() if descricao else ""
  ```
- **Impacto:** Ataques de Cross-Site Scripting (XSS) Armazenado, onde scripts maliciosos são executados no navegador de qualquer pessoa que visualize o feed de postagens.
- **Severidade:** 🟠 Alta
- **Recomendação:** Utilizar uma biblioteca de sanitização (ex: `bleach`) para filtrar o conteúdo antes de salvar no banco de dados.
- **Referências:** CWE-79 (XSS), OWASP A03:2021 (Injection).

### V07: Exposição de Interface de Rede (0.0.0.0)
- **Localização:** `run.py`, linha 4.
- **Descrição:** O host `0.0.0.0` faz com que a aplicação escute em todas as interfaces de rede do servidor.
- **Evidência:** `app.run(host="0.0.0.0", ...)`
- **Impacto:** Expõe a aplicação diretamente a redes externas ou redes internas não confiáveis se o servidor não estiver atrás de um firewall ou proxy reverso configurado corretamente.
- **Severidade:** 🟡 Média
- **Recomendação:** Configurar para `127.0.0.1` e utilizar um proxy reverso (Nginx/Gunicorn) para exposição externa.
- **Referências:** CWE-668 (Exposure of Resource to Wrong Sphere).

### V08: Processamento em Segundo Plano sem Limites (DoS)
- **Localização:** `app/jobs.py`, função `background_process_post`.
- **Descrição:** O sistema cria uma nova thread de sistema para cada postagem criada, sem utilizar um pool limitado.
- **Evidência:** 
  ```python
  thread = threading.Thread(target=task)
  thread.start()
  ```
- **Impacto:** Um ataque simples de volume pode causar exaustão de threads e memória (Negação de Serviço), derrubando o servidor.
- **Severidade:** 🟡 Média
- **Recomendação:** Implementar um `ThreadPoolExecutor` com limite fixo ou utilizar filas de tarefas como Celery ou RQ.
- **Referências:** CWE-400 (Uncontrolled Resource Consumption).

### V09: Dependências sem Versões Fixas
- **Localização:** `requirements.txt`.
- **Descrição:** As bibliotecas necessárias são listadas sem versões específicas (ex: `Flask` em vez de `Flask==3.1.3`).
- **Evidência:** Conteúdo do arquivo `requirements.txt`.
- **Impacto:** Risco de instalar versões com novas vulnerabilidades ou alterações que quebrem a segurança da aplicação durante o processo de build.
- **Severidade:** 🟡 Média
- **Recomendação:** Utilizar `pip freeze` para travar as versões exatas de todas as dependências.
- **Referências:** OWASP A06:2021 (Vulnerable and Outdated Components).

### V10: Uso de SQLite em Produção
- **Localização:** `app/__init__.py`.
- **Descrição:** A aplicação persiste dados em um arquivo local SQLite em um ambiente de contêineres.
- **Evidência:** `app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"`
- **Impacto:** Problemas de integridade de dados em acessos concorrentes e dificuldades na persistência em arquiteturas de contêineres efêmeros (sem volumes persistentes adequados).
- **Severidade:** 🔵 Baixa
- **Recomendação:** Migrar para um banco de dados cliente-servidor robusto como PostgreSQL ou MySQL.
- **Referências:** CWE-1065 (Runtime Database System Selection).
