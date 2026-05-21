# Relatório de Inspeção de Segurança - Fase 1 (Superficial)

Este relatório detalha as vulnerabilidades identificadas na fase inicial de inspeção do projeto **Sistema de Microblog**, focando em configurações globais e infraestrutura.

## 1. Resumo Executivo

| Severidade | Quantidade |
| :--- | :--- |
| Crítica | 1 |
| Alta | 2 |
| Média | 2 |
| Baixa | 0 |

---

## 2. Detalhes das Vulnerabilidades

### V1. Falha de Controle de Acesso (A01: Broken Access Control)
- **Local:** Geral (Rotas CRUD)
- **Descrição:** O sistema não possui nenhum mecanismo de autenticação ou autorização. Qualquer usuário pode acessar `/postagens/nova`, `/postagens/editar/<id>` e `/postagens/deletar/<id>`.
- **Severidade:** **Crítica**
- **Solução:** Implementar um sistema de login (ex: Flask-Login) e proteger rotas administrativas.

### V2. Modo de Depuração Ativo em Produção (A05: Security Misconfiguration)
- **Local:** `run.py`
- **Descrição:** A aplicação é iniciada com `debug=True`. Isso pode expor detalhes internos do servidor, variáveis de ambiente e código-fonte em caso de exceções não tratadas.
- **Severidade:** **Alta**
- **Solução:** Utilizar uma variável de ambiente para controlar o modo debug e garantir que seja `False` em produção.

### V3. Chave Secreta Exposta/Padrão (A05: Security Misconfiguration)
- **Local:** `app/__init__.py`
- **Descrição:** A `SECRET_KEY` possui um valor padrão (`'default-key'`). Se a variável de ambiente não for configurada, o sistema usará uma chave previsível, facilitando ataques de falsificação de sessão.
- **Severidade:** **Alta**
- **Solução:** Remover o valor padrão e forçar a falha da aplicação se a `SECRET_KEY` não for fornecida via ambiente.

### V4. Dependências Não Fixadas (A06: Vulnerable and Outdated Components)
- **Local:** `requirements.txt`
- **Descrição:** As bibliotecas não possuem versões especificadas (ex: `Flask` em vez de `Flask==3.1.3`). Isso permite a instalação automática de versões com vulnerabilidades conhecidas ou alterações incompatíveis.
- **Severidade:** **Média**
- **Solução:** Fixar as versões exatas de todas as dependências após auditoria.

### V5. Execução do Contêiner como Root (A05: Security Misconfiguration)
- **Local:** `Dockerfile`
- **Descrição:** O contêiner não define um usuário não privilegiado para rodar a aplicação. Em caso de comprometimento, o atacante terá privilégios de root no contêiner.
- **Severidade:** **Média**
- **Solução:** Criar um usuário sem privilégios (ex: `appuser`) no Dockerfile e usar a instrução `USER`.

---

## 3. As 5 Ações Mais Urgentes

1. **Desativar o modo Debug** no arquivo `run.py`.
2. **Remover a chave secreta padrão** e configurar uma chave forte via `.env`.
3. **Implementar autenticação básica** para restringir o acesso às rotas de criação, edição e exclusão.
4. **Fixar as versões das dependências** no arquivo `requirements.txt`.
5. **Configurar um usuário não-root** no `Dockerfile` para execução da aplicação.
