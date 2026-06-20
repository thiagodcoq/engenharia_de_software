"""Testes unitários para repositórios (implementações concretas)."""

import pytest
from datetime import date
from src.core.entities import Transacao, Categoria
from tests.conftest import MockTransacaoRepository, MockCategoriaRepository


class TestMockTransacaoRepository:
    """Testes para o repositório mock de transações."""

    def test_salvar_transacao_nova(self, mock_transacao_repo):
        """Testa salvamento de nova transação."""
        transacao = Transacao(
            id=None,
            usuario_id=1,
            categoria_id=1,
            descricao="Teste",
            valor=100.0,
            tipo="SAIDA",
            data=date.today()
        )

        resultado = mock_transacao_repo.salvar(transacao)

        assert resultado.id is not None
        assert resultado.id == 1

    def test_salvar_transacao_existente_atualiza(self, mock_transacao_repo):
        """Testa atualização de transação existente."""
        # Salva transação inicial
        transacao = Transacao(
            id=None,
            usuario_id=1,
            categoria_id=1,
            descricao="Original",
            valor=100.0,
            tipo="SAIDA",
            data=date.today()
        )
        transacao = mock_transacao_repo.salvar(transacao)

        # Atualiza transação
        transacao.descricao = "Atualizada"
        transacao.valor = 150.0
        resultado = mock_transacao_repo.salvar(transacao)

        assert resultado.descricao == "Atualizada"
        assert resultado.valor == 150.0

    def test_buscar_por_usuario(self, mock_transacao_repo):
        """Testa busca de transações por usuário."""
        # Adiciona transações para usuário 1
        t1 = Transacao(id=None, usuario_id=1, categoria_id=1, descricao="T1", valor=100.0, tipo="SAIDA", data=date.today())
        t2 = Transacao(id=None, usuario_id=1, categoria_id=2, descricao="T2", valor=200.0, tipo="ENTRADA", data=date.today())

        # Adiciona transação para usuário 2
        t3 = Transacao(id=None, usuario_id=2, categoria_id=1, descricao="T3", valor=300.0, tipo="SAIDA", data=date.today())

        mock_transacao_repo.salvar(t1)
        mock_transacao_repo.salvar(t2)
        mock_transacao_repo.salvar(t3)

        resultado = mock_transacao_repo.buscar_por_usuario(1)

        assert len(resultado) == 2
        assert all(t.usuario_id == 1 for t in resultado)

    def test_deletar_transacao(self, mock_transacao_repo):
        """Testa exclusão de transação."""
        transacao = Transacao(
            id=None,
            usuario_id=1,
            categoria_id=1,
            descricao="Teste",
            valor=100.0,
            tipo="SAIDA",
            data=date.today()
        )
        transacao = mock_transacao_repo.salvar(transacao)

        resultado = mock_transacao_repo.deletar(transacao.id, usuario_id=1)

        assert resultado is True
        assert mock_transacao_repo.buscar_por_usuario(1) == []

    def test_deletar_transacao_usuario_diferente_falha(self, mock_transacao_repo):
        """Testa que deleção por usuário diferente falha."""
        transacao = Transacao(
            id=None,
            usuario_id=1,
            categoria_id=1,
            descricao="Teste",
            valor=100.0,
            tipo="SAIDA",
            data=date.today()
        )
        transacao = mock_transacao_repo.salvar(transacao)

        resultado = mock_transacao_repo.deletar(transacao.id, usuario_id=2)

        assert resultado is False
        assert len(mock_transacao_repo.buscar_por_usuario(1)) == 1


class TestMockCategoriaRepository:
    """Testes para o repositório mock de categorias."""

    def test_salvar_categoria_nova(self, mock_categoria_repo):
        """Testa salvamento de nova categoria."""
        categoria = Categoria(
            id=None,
            usuario_id=1,
            nome="Alimentação",
            teto=500.0
        )

        resultado = mock_categoria_repo.salvar(categoria)

        assert resultado.id is not None
        assert resultado.id == 1

    def test_salvar_categoria_existente_atualiza(self, mock_categoria_repo):
        """Testa atualização de categoria existente."""
        categoria = Categoria(id=None, usuario_id=1, nome="Original", teto=100.0)
        categoria = mock_categoria_repo.salvar(categoria)

        categoria.nome = "Atualizada"
        categoria.teto = 200.0
        resultado = mock_categoria_repo.salvar(categoria)

        assert resultado.nome == "Atualizada"
        assert resultado.teto == 200.0

    def test_buscar_por_usuario(self, mock_categoria_repo):
        """Testa busca de categorias por usuário."""
        # Adiciona categorias para usuário 1
        c1 = Categoria(id=None, usuario_id=1, nome="Alimentação", teto=500.0)
        c2 = Categoria(id=None, usuario_id=1, nome="Transporte", teto=200.0)

        # Adiciona categoria para usuário 2
        c3 = Categoria(id=None, usuario_id=2, nome="Saúde", teto=300.0)

        mock_categoria_repo.salvar(c1)
        mock_categoria_repo.salvar(c2)
        mock_categoria_repo.salvar(c3)

        resultado = mock_categoria_repo.buscar_por_usuario(1)

        assert len(resultado) == 2
        assert all(c.usuario_id == 1 for c in resultado)

    def test_buscar_por_usuario_vazio(self, mock_categoria_repo):
        """Testa busca quando usuário não tem categorias."""
        resultado = mock_categoria_repo.buscar_por_usuario(99)

        assert resultado == []
