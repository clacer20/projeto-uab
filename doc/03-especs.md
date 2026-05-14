# Especificações Técnicas - Sistema de Microblog

## Inicialização Automática do Banco de Dados

### Problema Identificado
O sistema apresentava um erro `sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: postagem` ao ser iniciado pela primeira vez ou em ambientes limpos. Isso ocorria porque as tabelas do banco de dados não estavam sendo criadas automaticamente na inicialização do Flask, exigindo intervenção manual.

### Solução Implementada
Foi corrigida a lógica de inicialização no arquivo `app/__init__.py`. 

1. **Reordenação de Imports:** Os modelos da aplicação (`models.py`) foram movidos para serem importados antes da chamada `db.create_all()`. Isso garante que o SQLAlchemy tenha conhecimento de todas as classes de modelos (como a classe `Postagem`) antes de tentar gerar o esquema no banco de dados.
2. **Contexto da Aplicação:** A criação das tabelas foi encapsulada dentro de um bloco `with app.app_context():`, garantindo que o banco de dados seja inicializado corretamente dentro do ciclo de vida da aplicação Flask.

### Impacto
Toda vez que o container Docker for iniciado ou o comando `run.py` for executado, o sistema verificará a existência das tabelas no SQLite (`instance/app.db`) e as criará automaticamente caso não existam, eliminando a necessidade de comandos manuais e garantindo que o sistema esteja pronto para uso imediato.
