\#\# 4\. Especificação (Spec)

\#\#\# Arquivos de Configuração e Infraestrutura

\`\`\`text  
/requirements.txt  
ação: criar  
descrição: Definição das bibliotecas e dependências do Python necessárias para a execução do projeto.  
pseudocódigo:  
ADICIONAR "Flask"  
ADICIONAR "Flask-SQLAlchemy"  
ADICIONAR "python-dotenv"  
\`\`\`

\`\`\`text  
/Dockerfile  
ação: criar  
descrição: Especificação das instruções para a criação da imagem do contêiner Docker contendo o ambiente Python.  
pseudocódigo:  
DEFINIR imagem base como "python:3.10-slim"  
DEFINIR diretório de trabalho como "/app"  
COPIAR "requirements.txt" para "/app"  
EXECUTAR comando "pip install \-r requirements.txt"  
COPIAR todo o conteúdo do diretório atual para "/app"  
EXPÔR a porta 5000  
DEFINIR comando de inicialização: "python run.py"  
\`\`\`

\`\`\`text  
/docker-compose.yml  
ação: criar  
descrição: Orquestração do contêiner da aplicação e mapeamento do volume para persistência do banco de dados SQLite.  
pseudocódigo:  
DEFINIR versão do docker-compose como "3.8"  
INICIAR bloco de serviços:  
  SERVIÇO "web":  
    CONSTRUIR a partir do diretório atual "."  
    MAPEAMENTO de portas: "5000:5000"  
    MAPEAMENTO de volumes: "sqlite\_data" para o caminho "/app/instance"  
    ARQUIVO de ambiente: ".env"  
INICIAR bloco de volumes:  
  DECLARAR volume "sqlite\_data"  
\`\`\`

\`\`\`text  
/run.py  
ação: criar  
descrição: Ponto de entrada (entrypoint) para iniciar o servidor web da aplicação Flask.  
pseudocódigo:  
IMPORTAR "app" do módulo "app"  
SE o script for executado diretamente (\_\_name\_\_ \== '\_\_main\_\_'):  
  EXECUTAR app.run(host="0.0.0.0", port=5000, debug=VERDADEIRO se ambiente for desenvolvimento)  
\`\`\`

\#\#\# Arquivos da Aplicação (Backend)

\`\`\`text  
/app/\_\_init\_\_.py  
ação: criar  
descrição: Inicialização do microsserviço Flask, carregamento de variáveis de ambiente e configuração do banco de dados.  
pseudocódigo:  
IMPORTAR Flask  
IMPORTAR SQLAlchemy  
IMPORTAR load\_dotenv  
EXECUTAR load\_dotenv() para ler ".env"  
INSTANCIAR aplicativo Flask em variável "app"  
CONFIGURAR app.config['SECRET_KEY'] a partir do ambiente  
CONFIGURAR app.config['SQLALCHEMY_DATABASE_URI'] a partir do ambiente (padrão: "sqlite:///app.db")  
CONFIGURAR app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] como FALSO  
INSTANCIAR SQLAlchemy passando "app", salvar em variável "db"  
IMPORTAR módulo "models" (do pacote app)  
IMPORTAR módulo "routes" (do pacote app)  
CRIAR todas as tabelas do banco de dados executando "db.create_all()" dentro do contexto do app ("with app.app_context()")  
\`\`\`

\`\`\`text  
/app/models.py  
ação: criar  
descrição: Definição da estrutura da tabela de banco de dados para a entidade Postagem.  
pseudocódigo:  
IMPORTAR "db" de "app"  
CRIAR classe "Postagem" herdando de "db.Model":  
  DEFINIR coluna "id" como Inteiro, Chave Primária  
  DEFINIR coluna "titulo" como String(100), Não Nula  
  DEFINIR coluna "descricao" como Texto, Não Nula  
\`\`\`

\`\`\`text  
/app/routes.py  
ação: criar  
descrição: Implementação dos controladores (controllers) responsáveis pelas rotas CRUD e regras de negócio.  
pseudocódigo:  
IMPORTAR "app" e "db" de "app"  
IMPORTAR "Postagem" de "app.models"  
IMPORTAR métodos auxiliares do Flask (render\_template, request, redirect, url\_for)

DEFINIR ROTA "/" (MÉTODOS: GET):  
  BUSCAR todas as postagens no banco de dados, ordenando por "id" decrescente  
  RETORNAR render\_template("index.html", postagens=resultado\_da\_busca)

DEFINIR ROTA "/postagens/nova" (MÉTODOS: GET, POST):  
  SE request.method for "POST":  
    EXTRAIR "titulo" e "descricao" do request.form  
    INSTANCIAR "nova\_postagem" com "titulo" e "descricao"  
    ADICIONAR "nova\_postagem" ao "db.session"  
    EXECUTAR "db.session.commit()"  
    RETORNAR redirect para ROTA "/"  
  SENÃO (GET):  
    RETORNAR render\_template("form.html", acao="Nova Postagem")

DEFINIR ROTA "/postagens/editar/\<int:id\>" (MÉTODOS: GET, POST):  
  BUSCAR postagem no banco de dados usando "id" (ou retornar 404 se não existir)  
  SE request.method for "POST":  
    ATUALIZAR postagem.titulo com request.form\['titulo'\]  
    ATUALIZAR postagem.descricao com request.form\['descricao'\]  
    EXECUTAR "db.session.commit()"  
    RETORNAR redirect para ROTA "/"  
  SENÃO (GET):  
    RETORNAR render\_template("form.html", acao="Editar Postagem", postagem=postagem)

DEFINIR ROTA "/postagens/deletar/\<int:id\>" (MÉTODOS: POST):  
  BUSCAR postagem no banco de dados usando "id" (ou retornar 404 se não existir)  
  REMOVER postagem do "db.session"  
  EXECUTAR "db.session.commit()"  
  RETORNAR redirect para ROTA "/"

DEFINIR ROTA "/relatorios" (MÉTODOS: GET):  
  CALCULAR total de registros na tabela Postagem  
  RETORNAR render\_template("relatorios.html", total\_postagens=total\_calculado)  
\`\`\`

\#\#\# Arquivos de Interface (Frontend / Templates)

\`\`\`text  
/app/templates/base.html  
ação: criar  
descrição: Template pai contendo a estrutura base do HTML, importação do Bootstrap e cabeçalho de navegação.  
pseudocódigo:  
DECLARAR tipo de documento HTML5  
INICIAR tag \<html\>  
INICIAR tag \<head\>:  
  ADICIONAR tag \<meta\> charset UTF-8  
  ADICIONAR tag \<meta\> viewport  
  ADICIONAR tag \<title\> "Sistema de Microblog"  
  ADICIONAR tag \<link\> apontando para o CSS do Bootstrap via CDN  
FECHAR \<head\>  
INICIAR tag \<body\>:  
  INICIAR tag \<nav\> (Barra de navegação):  
    ADICIONAR link para ROTA "/" com texto "Home"  
    ADICIONAR link para ROTA "/relatorios" com texto "Relatórios"  
  FECHAR \<nav\>  
  INICIAR tag \<main\> com classe container:  
    INSERIR bloco Jinja "{% block content %}"  
    INSERIR bloco Jinja "{% endblock %}"  
  FECHAR \<main\>  
FECHAR \<body\>  
FECHAR \<html\>  
\`\`\`

\`\`\`text  
/app/templates/index.html  
ação: criar  
descrição: Interface principal que lista as postagens existentes e oferece atalhos para criação, edição e exclusão.  
pseudocódigo:  
ESTENDER template "base.html"  
INICIAR bloco "content":  
  ADICIONAR título \<h1\> "Feed de Postagens"  
  ADICIONAR botão \<a\> apontando para ROTA "/postagens/nova" com texto "Nova Postagem"  
  INICIAR loop Jinja "{% for post in postagens %}":  
    INICIAR estrutura de Card do Bootstrap:  
      EXIBIR "post.titulo" no cabeçalho do card  
      EXIBIR "post.descricao" no corpo do card  
      INICIAR formulário de exclusão apontando para ROTA "/postagens/deletar/post.id" (Método POST):  
        ADICIONAR link de edição \<a\> apontando para ROTA "/postagens/editar/post.id" com texto "Editar"  
        ADICIONAR botão de submissão \<button\> com texto "Apagar"  
      FECHAR formulário de exclusão  
    FECHAR estrutura de Card  
  FECHAR loop Jinja  
FECHAR bloco "content"  
\`\`\`

\`\`\`text  
/app/templates/form.html  
ação: criar  
descrição: Formulário dinâmico utilizado tanto para cadastrar novas postagens quanto para atualizar as existentes.  
pseudocódigo:  
ESTENDER template "base.html"  
INICIAR bloco "content":  
  EXIBIR variável de título "{{ acao }}" na tag \<h2\>  
  INICIAR tag \<form\> com método POST (action vazia submete para a rota atual):  
    INICIAR grupo de input para Título:  
      ADICIONAR \<label\> "Título"  
      ADICIONAR \<input type="text" name="titulo"\>  
      SE "postagem" existir (modo edição), PREENCHER o atributo "value" com "postagem.titulo"  
      MARCAR como "required"  
    INICIAR grupo de input para Descrição:  
      ADICIONAR \<label\> "Descrição"  
      ADICIONAR \<textarea name="descricao"\>  
      SE "postagem" existir (modo edição), PREENCHER o conteúdo com "postagem.descricao"  
      MARCAR como "required"  
    ADICIONAR botão \<button type="submit"\> com texto "Salvar"  
    ADICIONAR link \<a\> apontando para ROTA "/" com texto "Cancelar"  
  FECHAR tag \<form\>  
FECHAR bloco "content"  
\`\`\`

\`\`\`text  
/app/templates/relatorios.html  
ação: criar  
descrição: Interface para visualização de métricas e indicadores de volume gerenciais.  
pseudocódigo:  
ESTENDER template "base.html"  
INICIAR bloco "content":  
  ADICIONAR título \<h2\> "Relatórios Gerenciais"  
  INICIAR estrutura de Card do Bootstrap:  
    EXIBIR texto "Métricas de Volume de Conteúdo"  
    INICIAR lista \<ul\>:  
      ADICIONAR item \<li\>: "Total de Postagens Cadastradas: {{ total\_postagens }}"  
    FECHAR lista  
  FECHAR estrutura de Card  
FECHAR bloco "content"  
\`\`\`