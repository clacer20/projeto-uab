import pytest
from app import app, db
from app.models import Postagem

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_criar_postagem_sucesso(client):
    """T1: Validar criação de postagem com sucesso"""
    response = client.post('/postagens/nova', data={
        'titulo': 'Post de Teste',
        'descricao': 'Descrição do teste'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Post de Teste' in response.data
    
    post = Postagem.query.first()
    assert post.titulo == 'Post de Teste'

def test_editar_postagem_sucesso(client):
    """T3: Validar edição de postagem existente"""
    # Criar uma postagem inicial
    post = Postagem(titulo='Original', descricao='Original')
    db.session.add(post)
    db.session.commit()
    
    response = client.post(f'/postagens/editar/{post.id}', data={
        'titulo': 'Editado',
        'descricao': 'Editado'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    db.session.refresh(post)
    assert post.titulo == 'Editado'

def test_deletar_postagem_sucesso(client):
    """T4: Validar exclusão de postagem"""
    post = Postagem(titulo='Para Deletar', descricao='Deletar')
    db.session.add(post)
    db.session.commit()
    
    response = client.post(f'/postagens/deletar/{post.id}', follow_redirects=True)
    
    assert response.status_code == 200
    assert Postagem.query.get(post.id) is None

def test_listagem_ordem_decrescente(client):
    """T5: Validar se as postagens aparecem em ordem decrescente de ID"""
    p1 = Postagem(titulo='Primeiro', descricao='Primeiro')
    p2 = Postagem(titulo='Segundo', descricao='Segundo')
    db.session.add_all([p1, p2])
    db.session.commit()
    
    response = client.get('/')
    # O "Segundo" deve aparecer antes do "Primeiro" no HTML
    index_primeiro = response.data.find(b'Primeiro')
    index_segundo = response.data.find(b'Segundo')
    assert index_segundo < index_primeiro

def test_relatorio_total_postagens(client):
    """T6: Validar o contador de relatórios"""
    p1 = Postagem(titulo='A', descricao='A')
    p2 = Postagem(titulo='B', descricao='B')
    db.session.add_all([p1, p2])
    db.session.commit()
    
    response = client.get('/relatorios')
    assert b'Total de Postagens Cadastradas: 2' in response.data
