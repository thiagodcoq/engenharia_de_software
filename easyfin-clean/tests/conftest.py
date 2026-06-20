"""Configuração e fixtures para testes do projeto EasyFin."""

import pytest
import tempfile
import os
from datetime import date
from src.core.entities import Usuario, Categoria, Transacao
from src.core.repositories import TransacaoRepositoryInterface, CategoriaRepositoryInterface
from src.infrastructure.web.app import create_app
from src.infrastructure.database import db


class MockTransacaoRepository(TransacaoRepositoryInterface):
    """Repository mock para testes de transações."""

    def __init__(self):
        self.transacoes = {}
        self.next_id = 1

    def salvar(self, transacao):
        if transacao.id is None:
            transacao.id = self.next_id
            self.next_id += 1
        self.transacoes[transacao.id] = transacao
        return transacao

    def buscar_por_usuario(self, usuario_id, limite=20):
        return [
            t for t in self.transacoes.values()
            if t.usuario_id == usuario_id
        ][:limite]

    def deletar(self, transacao_id, usuario_id):
        if transacao_id in self.transacoes:
            t = self.transacoes[transacao_id]
            if t.usuario_id == usuario_id:
                del self.transacoes[transacao_id]
                return True
        return False


class MockCategoriaRepository(CategoriaRepositoryInterface):
    """Repository mock para testes de categorias."""

    def __init__(self):
        self.categorias = {}
        self.next_id = 1

    def buscar_por_usuario(self, usuario_id):
        return [c for c in self.categorias.values() if c.usuario_id == usuario_id]

    def salvar(self, categoria):
        if categoria.id is None:
            categoria.id = self.next_id
            self.next_id += 1
        self.categorias[categoria.id] = categoria
        return categoria


@pytest.fixture
def mock_transacao_repo():
    """Fixture: repositório mock de transações."""
    return MockTransacaoRepository()


@pytest.fixture
def mock_categoria_repo():
    """Fixture: repositório mock de categorias."""
    return MockCategoriaRepository()


@pytest.fixture
def usuario_fixture():
    """Fixture: entidade de usuário para testes."""
    return Usuario(
        id=1,
        nome="João Silva",
        email="joao@example.com",
        senha_hash="hashed_password_123"
    )


@pytest.fixture
def categoria_fixture(usuario_fixture):
    """Fixture: entidade de categoria para testes."""
    return Categoria(
        id=None,
        usuario_id=usuario_fixture.id,
        nome="Alimentação",
        teto=500.0
    )


@pytest.fixture
def transacao_fixture(usuario_fixture, categoria_fixture):
    """Fixture: entidade de transação para testes."""
    return Transacao(
        id=None,
        usuario_id=usuario_fixture.id,
        categoria_id=categoria_fixture.id,
        descricao="Compra no supermercado",
        valor=150.50,
        tipo="SAIDA",
        data=date.today()
    )


# ============================================================================
# FIXTURES DE BANCO DE DADOS REAL (para testes de integração)
# ============================================================================

@pytest.fixture
def app_test():
    """Fixture: app Flask com banco de dados de teste (em memória)."""
    # Usa banco de dados em memória para testes rápidos
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def db_session(app_test):
    """Fixture: sessão do banco de dados para testes."""
    with app_test.app_context():
        yield db


@pytest.fixture
def usuario_no_db(db_session):
    """Fixture: usuário salvo no banco de dados real."""
    from src.infrastructure.database.models import DBUsuario
    
    usuario = DBUsuario(nome="João Silva", email="joao@test.com")
    usuario.set_password("senha123")
    db_session.session.add(usuario)
    db_session.session.commit()
    return usuario


@pytest.fixture
def categoria_no_db(db_session, usuario_no_db):
    """Fixture: categoria salva no banco de dados real."""
    from src.infrastructure.database.models import DBCategoria
    
    categoria = DBCategoria(
        usuario_id=usuario_no_db.id,
        nome="Alimentação",
        teto=500.0
    )
    db_session.session.add(categoria)
    db_session.session.commit()
    return categoria

