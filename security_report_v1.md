# Relatório de Inspeção de Segurança - Fase 1: Superficial

Este relatório detalha a inspeção de cibersegurança de nível superficial do projeto **Sistema de Microblog**, focando em infraestrutura, configurações e dependências.

## 1. Resumo Executivo

| Severidade | Quantidade |
| :--- | :--- |
| Crítica | 1 |
| Alta | 2 |
| Média | 2 |
| Baixa | 1 |
| **Total** | **6** |

## 2. Detalhamento de Vulnerabilidades

### V01: Modo Debug Ativado em Produção (A05: Security Misconfiguration)
- **Informação:** O arquivo `run.py` inicia a aplicação com `debug=True`.
- **Impacto:** Expõe tracebacks detalhados, variáveis de ambiente e pode permitir a execução remota de código (RCE) através do console interativo do debugger.
- **Sugestão de Solução:** Definir `debug=False` por padrão ou utilizar variáveis de ambiente para controlar o estado.

### V02: Execução como Usuário Root no Docker (A05: Security Misconfiguration)
- **Informação:** O `Dockerfile` não define um usuário não privilegiado.
- **Impacto:** Se um invasor comprometer a aplicação, ele terá privilégios de root dentro do contêiner, facilitando ataques de "container breakout".
- **Sugestão de Solução:** Criar um usuário no `Dockerfile` e utilizar a instrução `USER`.

### V03: Ausência de Proteção CSRF (A01: Broken Access Control)
- **Informação:** A aplicação não utiliza `Flask-WTF` ou qualquer mecanismo de proteção contra Cross-Site Request Forgery (CSRF).
- **Impacto:** Um invasor pode induzir um usuário autenticado a realizar ações indesejadas (como deletar postagens) através de sites maliciosos.
- **Sugestão de Solução:** Instalar e configurar o `SeaSurf` ou `Flask-WTF` para proteção automática de formulários POST.

### V04: Chave Secreta Fraca ou Padrão (A02: Cryptographic Failures)
- **Informação:** Em `app/__init__.py`, a `SECRET_KEY` possui um fallback para `'default-key'`.
- **Impacto:** Facilita ataques de força bruta em sessões se a variável de ambiente não estiver definida corretamente.
- **Sugestão de Solução:** Forçar a falha da aplicação se a chave não estiver no `.env` ou gerar uma chave criptograficamente forte.

### V05: Dependências sem Versões Fixas (A06: Vulnerable and Outdated Components)
- **Informação:** O `requirements.txt` lista pacotes sem fixar versões específicas (ex: `Flask`).
- **Impacto:** Pode introduzir vulnerabilidades conhecidas em versões futuras ou quebras de funcionalidade.
- **Sugestão de Solução:** Fixar versões no `requirements.txt` utilizando `pip freeze`.

### V06: Ausência de Cabeçalhos de Segurança (A05: Security Misconfiguration)
- **Informação:** A aplicação não configura cabeçalhos como `Content-Security-Policy`, `X-Frame-Options` ou `Strict-Transport-Security`.
- **Impacto:** Aumenta a exposição a ataques de XSS e Clickjacking.
- **Sugestão de Solução:** Utilizar extensões como `Flask-Talisman`.

## 3. As 5 Ações Mais Urgentes

1. **Desativar o modo Debug** (`debug=False`) em ambientes que não sejam de desenvolvimento local.
2. **Implementar Proteção CSRF** em todas as rotas de modificação de dados (POST).
3. **Configurar um usuário não-root** no Dockerfile para isolamento de privilégios.
4. **Fixar as versões das dependências** no `requirements.txt`.
5. **Garantir o uso de uma `SECRET_KEY` forte** e remover fallbacks inseguros.
