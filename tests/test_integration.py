import pytest
from app import app, db
from app.models import Postagem

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Use a separate test database file to ensure real file operations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_integration.db'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_full_flow_integration(client):
    """
    Teste de Integração Completo:
    1. Backend/Banco: Verifica se o banco inicia vazio.
    2. Frontend/Backend: Simula envio de formulário (POST).
    3. Banco: Verifica persistência real dos dados.
    4. Frontend: Verifica se o dado persistido aparece na listagem (GET).
    """
    
    # 1. Isolamento Backend/Banco: Verificar estado inicial
    with app.app_context():
        assert Postagem.query.count() == 0

    # 2. Frontend/Backend: Criar postagem via rota
    response_post = client.post('/postagens/nova', data={
        'titulo': 'Titulo Integracao',
        'descricao': 'Descricao Integracao'
    }, follow_redirects=True)
    
    assert response_post.status_code == 200
    
    # 3. Isolamento Banco: Validar que o registro existe no banco
    with app.app_context():
        post = Postagem.query.filter_by(titulo='Titulo Integracao').first()
        assert post is not None
        assert post.descricao == 'Descricao Integracao'

    # 4. Frontend: Validar que o registro aparece no HTML (Listagem)
    response_get = client.get('/')
    assert b'Titulo Integracao' in response_get.data
    assert b'Descricao Integracao' in response_get.data

def test_backend_logic_isolation():
    """Teste isolado da lógica do modelo (Backend/Banco)"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        p = Postagem(titulo='Teste Unitario', descricao='Lógica pura')
        db.session.add(p)
        db.session.commit()
        
        assert p.id is not None
        assert Postagem.query.get(p.id).titulo == 'Teste Unitario'
        db.drop_all()

def test_frontend_rendering_isolation(client):
    """Teste isolado de renderização de rotas (Frontend)"""
    # Verifica se a página de relatórios carrega o template corretamente
    response = client.get('/relatorios')
    assert response.status_code == 200
    assert b'Relat' in response.data # Verifica parte do título no HTML
    assert b'Total de Postagens' in response.data
