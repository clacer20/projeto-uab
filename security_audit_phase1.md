# Relatório de Inspeção de Segurança - Nível Superficial (Fase 1)

Este relatório detalha as vulnerabilidades de cibersegurança identificadas durante a primeira fase de inspeção (Superficial) do projeto **Sistema de Microblog**.

## 1. Resumo Executivo

| Severidade | Quantidade |
| :--- | :--- |
| Crítica | 1 |
| Alta | 2 |
| Média | 2 |
| Baixa | 1 |
| **Total** | **6** |

## 2. Vulnerabilidades Identificadas

### V1: Modo de Depuração Ativo em Produção (Severidade: Crítica)
- **Descrição:** O arquivo `run.py` executa a aplicação com `debug=True`. Isso expõe rastros de pilha (stack traces) e informações do sistema em caso de erro, além de possibilitar execução remota de código via o depurador interativo do Werkzeug se não protegido.
- **OWASP:** [A05:2021 – Security Misconfiguration](https://owasp.org/Top10/A05-Security-Misconfiguration/)
- **Sugestão de Solução:** Definir `debug=False` por padrão ou utilizar uma variável de ambiente (ex: `FLASK_DEBUG`) para controlar o estado.

### V2: Chave Secreta Exposta/Fraca (Severidade: Alta)
- **Descrição:** O arquivo `app/__init__.py` define uma chave padrão `'default-key'`. Chaves fracas ou conhecidas facilitam ataques de falsificação de sessão (Session Hijacking/Fixation).
- **OWASP:** [A02:2021 – Cryptographic Failures](https://owasp.org/Top10/A02-Cryptographic-Failures/)
- **Sugestão de Solução:** Remover o valor padrão e exigir que a `SECRET_KEY` seja fornecida via variável de ambiente. Em produção, utilizar chaves geradas aleatoriamente e complexas.

### V3: Execução como Usuário Root no Docker (Severidade: Alta)
- **Descrição:** O `Dockerfile` não define um usuário sem privilégios. Por padrão, a aplicação roda como `root` dentro do contêiner, o que aumenta o impacto de uma possível invasão.
- **Melhor Prática:** Segurança de Contêineres.
- **Sugestão de Solução:** Criar um usuário de sistema (ex: `pythonuser`) no Dockerfile e utilizar a instrução `USER` para executar o processo.

### V4: Dependências Não Fixadas (Severidade: Média)
- **Descrição:** O arquivo `requirements.txt` lista bibliotecas sem especificar versões. Isso pode levar à instalação de versões com vulnerabilidades conhecidas ou alterações que quebrem a segurança.
- **OWASP:** [A06:2021 – Vulnerable and Outdated Components](https://owasp.org/Top10/A06-Vulnerable-and-Outdated-Components/)
- **Sugestão de Solução:** Utilizar `pip freeze > requirements.txt` para fixar as versões exatas das dependências.

### V5: Falta de Cabeçalhos de Segurança (Severidade: Média)
- **Descrição:** A aplicação não configura cabeçalhos HTTP de segurança básicos (HSTS, CSP, X-Frame-Options, X-Content-Type-Options).
- **OWASP:** [A05:2021 – Security Misconfiguration](https://owasp.org/Top10/A05-Security-Misconfiguration/)
- **Sugestão de Solução:** Implementar extensões como `Flask-Talisman` para gerenciar cabeçalhos de segurança automaticamente.

### V6: Exposição de Caminhos Internos em Logs (Severidade: Baixa)
- **Descrição:** O `print` do URI do banco de dados em `app/__init__.py` expõe caminhos absolutos do sistema de arquivos nos logs do contêiner.
- **Sugestão de Solução:** Remover logs de depuração que contenham caminhos sensíveis em ambientes de produção.

## 3. As 5 Ações Mais Urgentes

1.  **Desativar o modo Debug** no `run.py`.
2.  **Configurar uma SECRET_KEY forte** via variável de ambiente.
3.  **Alterar o usuário no Dockerfile** de `root` para um usuário sem privilégios.
4.  **Fixar versões das dependências** no `requirements.txt`.
5.  **Remover logs de depuração** que expõem caminhos de arquivos.
