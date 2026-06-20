"""Configuração e fixtures para testes do projeto EasyFin."""

import pytest
from datetime import date
from src.core.entities import Usuario, Categoria, Transacao
from src.core.repositories import TransacaoRepositoryInterface, CategoriaRepositoryInterface


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
