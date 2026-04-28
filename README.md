# Sistema de Microblog (Projeto UAB)

Este é um sistema de microblog funcional desenvolvido com **Flask** e **SQLAlchemy**, projetado para ser executado em um ambiente de contêineres utilizando **Docker**. O projeto permite o gerenciamento completo (CRUD) de postagens e a visualização de relatórios gerenciais simples.

## 🚀 Funcionalidades

- **Feed de Postagens:** Visualização de todas as postagens em ordem cronológica inversa.
- **Gerenciamento de Conteúdo:** Criação, edição e exclusão de postagens (Título e Descrição).
- **Relatórios:** Página dedicada para visualização de métricas (total de postagens cadastradas).
- **Interface Responsiva:** Interface limpa e moderna utilizando **Bootstrap 5**.
- **Persistência de Dados:** Banco de dados SQLite persistente através de volumes Docker.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.10, Flask, Flask-SQLAlchemy.
- **Frontend:** Jinja2 (Templates), Bootstrap 5 (CSS).
- **Infraestrutura:** Docker, Docker Compose.
- **Banco de Dados:** SQLite.

## 📋 Pré-requisitos

- [Docker](https://www.docker.com/get-started) instalado.
- [Docker Compose](https://docs.docker.com/compose/install/) instalado (opcional, recomendado).

## 🏃 Como Rodar a Aplicação

### Via Docker Compose (Recomendado)

1. Clone o repositório.
2. Na raiz do projeto, execute:
   ```bash
   docker-compose up --build
   ```
3. Acesse em seu navegador: [http://localhost:5000](http://localhost:5000)

### Via Docker CLI (Caso o Compose não esteja disponível)

1. Construa a imagem:
   ```bash
   docker build -t microblog-app .
   ```
2. Inicie o contêiner:
   ```bash
   docker run -d --name microblog-web -p 5000:5000 microblog-app
   ```

## 📁 Estrutura do Projeto

- `app/`: Contém o código-fonte da aplicação Flask.
  - `models.py`: Estrutura do banco de dados.
  - `routes.py`: Lógica de rotas e controladores.
  - `templates/`: Arquivos HTML (Jinja2).
- `run.py`: Ponto de entrada da aplicação.
- `Dockerfile`: Configuração da imagem Docker.
- `docker-compose.yml`: Orquestração de serviços e volumes.

---
Desenvolvido por **clacer20** como parte do Projeto UAB.
