"""Testes de integração para repositórios SQLAlchemy com banco de dados real."""

import pytest
from datetime import date
from src.core.entities import Transacao, Categoria
from src.infrastructure.database.repositories import (
    SQLAlchemyTransacaoRepository,
    SQLAlchemyCategoriaRepository
)
from src.infrastructure.database.models import DBTransacao, DBCategoria
from src.infrastructure.database import db


class TestSQLAlchemyTransacaoRepository:
    """Testes de integração para repositório SQLAlchemy de transações."""

    def test_salvar_transacao_nova_insere_no_banco(self, app_test, usuario_no_db, categoria_no_db):
        """Testa que transação nova é inserida no banco com ID gerado."""
        with app_test.app_context():
            repo = SQLAlchemyTransacaoRepository()
            
            transacao = Transacao(
                id=None,
                usuario_id=usuario_no_db.id,
                categoria_id=categoria_no_db.id,
                descricao="Teste compra",
                valor=100.0,
                tipo="SAIDA",
                data=date.today()
            )
            
            resultado = repo.salvar(transacao)
            
            assert resultado.id is not None
            # Verifica que realmente foi salvo no banco
            db_tx = DBTransacao.query.filter_by(id=resultado.id).first()
            assert db_tx is not None
            assert db_tx.descricao == "Teste compra"
            assert float(db_tx.valor) == 100.0

    def test_buscar_por_usuario_retorna_apenas_usuario(self, app_test, usuario_no_db, categoria_no_db):
        """Testa que busca retorna apenas transações do usuário."""
        with app_test.app_context():
            repo = SQLAlchemyTransacaoRepository()
            
            # Cria transações para usuário 1
            t1 = Transacao(id=None, usuario_id=usuario_no_db.id, categoria_id=categoria_no_db.id,
                          descricao="T1", valor=50.0, tipo="SAIDA", data=date.today())
            t2 = Transacao(id=None, usuario_id=usuario_no_db.id, categoria_id=categoria_no_db.id,
                          descricao="T2", valor=75.0, tipo="ENTRADA", data=date.today())
            
            repo.salvar(t1)
            repo.salvar(t2)
            
            # Cria transação para usuário 2 (não deve aparecer)
            t3 = Transacao(id=None, usuario_id=999, categoria_id=categoria_no_db.id,
                          descricao="T3", valor=200.0, tipo="SAIDA", data=date.today())
            repo.salvar(t3)
            
            # Busca transações do usuário 1
            resultado = repo.buscar_por_usuario(usuario_no_db.id)
            
            assert len(resultado) == 2
            assert all(t.usuario_id == usuario_no_db.id for t in resultado)

    def test_buscar_por_usuario_respeita_limite(self, app_test, usuario_no_db, categoria_no_db):
        """Testa que limite de transações é respeitado."""
        with app_test.app_context():
            repo = SQLAlchemyTransacaoRepository()
            
            # Cria 5 transações
            for i in range(5):
                t = Transacao(
                    id=None,
                    usuario_id=usuario_no_db.id,
                    categoria_id=categoria_no_db.id,
                    descricao=f"T{i}",
                    valor=float(i + 1) * 10,
                    tipo="SAIDA",
                    data=date.today()
                )
                repo.salvar(t)
            
            # Busca com limite de 3
            resultado = repo.buscar_por_usuario(usuario_no_db.id, limite=3)
            
            assert len(resultado) == 3

    def test_deletar_transacao_remove_do_banco(self, app_test, usuario_no_db, categoria_no_db):
        """Testa que deletar transação a remove do banco."""
        with app_test.app_context():
            repo = SQLAlchemyTransacaoRepository()
            
            transacao = Transacao(
                id=None,
                usuario_id=usuario_no_db.id,
                categoria_id=categoria_no_db.id,
                descricao="Teste",
                valor=50.0,
                tipo="SAIDA",
                data=date.today()
            )
            
            transacao = repo.salvar(transacao)
            assert DBTransacao.query.filter_by(id=transacao.id).first() is not None
            
            # Deleta
            resultado = repo.deletar(transacao.id, usuario_no_db.id)
            
            assert resultado is True
            assert DBTransacao.query.filter_by(id=transacao.id).first() is None

    def test_deletar_transacao_usuario_diferente_falha(self, app_test, usuario_no_db, categoria_no_db):
        """Testa que deletar por usuário diferente falha."""
        with app_test.app_context():
            repo = SQLAlchemyTransacaoRepository()
            
            transacao = Transacao(
                id=None,
                usuario_id=usuario_no_db.id,
                categoria_id=categoria_no_db.id,
                descricao="Teste",
                valor=50.0,
                tipo="SAIDA",
                data=date.today()
            )
            
            transacao = repo.salvar(transacao)
            
            # Tenta deletar com usuário diferente
            resultado = repo.deletar(transacao.id, usuario_id=999)
            
            assert resultado is False
            # Transação continua no banco
            assert DBTransacao.query.filter_by(id=transacao.id).first() is not None

    def test_atualizar_transacao_existente(self, app_test, usuario_no_db, categoria_no_db):
        """Testa que atualizar transação existente modifica no banco."""
        with app_test.app_context():
            repo = SQLAlchemyTransacaoRepository()
            
            transacao = Transacao(
                id=None,
                usuario_id=usuario_no_db.id,
                categoria_id=categoria_no_db.id,
                descricao="Original",
                valor=100.0,
                tipo="SAIDA",
                data=date.today()
            )
            
            transacao = repo.salvar(transacao)
            
            # Atualiza
            transacao.descricao = "Atualizada"
            transacao.valor = 150.0
            repo.salvar(transacao)
            
            # Verifica no banco
            db_tx = DBTransacao.query.filter_by(id=transacao.id).first()
            assert db_tx.descricao == "Atualizada"
            assert float(db_tx.valor) == 150.0


class TestSQLAlchemyCategoriaRepository:
    """Testes de integração para repositório SQLAlchemy de categorias."""

    def test_salvar_categoria_nova_insere_no_banco(self, app_test, usuario_no_db):
        """Testa que categoria nova é inserida no banco com ID gerado."""
        with app_test.app_context():
            repo = SQLAlchemyCategoriaRepository()
            
            categoria = Categoria(
                id=None,
                usuario_id=usuario_no_db.id,
                nome="Transporte",
                teto=200.0
            )
            
            resultado = repo.salvar(categoria)
            
            assert resultado.id is not None
            # Verifica que realmente foi salvo no banco
            db_cat = DBCategoria.query.filter_by(id=resultado.id).first()
            assert db_cat is not None
            assert db_cat.nome == "Transporte"
            assert float(db_cat.teto) == 200.0

    def test_buscar_por_usuario_retorna_apenas_usuario(self, app_test, usuario_no_db):
        """Testa que busca retorna apenas categorias do usuário."""
        with app_test.app_context():
            repo = SQLAlchemyCategoriaRepository()
            
            # Cria categorias para usuário 1
            c1 = Categoria(id=None, usuario_id=usuario_no_db.id, nome="Alimentação", teto=500.0)
            c2 = Categoria(id=None, usuario_id=usuario_no_db.id, nome="Saúde", teto=300.0)
            
            repo.salvar(c1)
            repo.salvar(c2)
            
            # Cria categoria para usuário 2 (não deve aparecer)
            c3 = Categoria(id=None, usuario_id=999, nome="Lazer", teto=400.0)
            repo.salvar(c3)
            
            # Busca categorias do usuário 1
            resultado = repo.buscar_por_usuario(usuario_no_db.id)
            
            assert len(resultado) == 2
            assert all(c.usuario_id == usuario_no_db.id for c in resultado)

    def test_atualizar_categoria_existente(self, app_test, usuario_no_db):
        """Testa que atualizar categoria existente modifica no banco."""
        with app_test.app_context():
            repo = SQLAlchemyCategoriaRepository()
            
            categoria = Categoria(
                id=None,
                usuario_id=usuario_no_db.id,
                nome="Original",
                teto=100.0
            )
            
            categoria = repo.salvar(categoria)
            
            # Atualiza
            categoria.nome = "Atualizada"
            categoria.teto = 200.0
            repo.salvar(categoria)
            
            # Verifica no banco
            db_cat = DBCategoria.query.filter_by(id=categoria.id).first()
            assert db_cat.nome == "Atualizada"
            assert float(db_cat.teto) == 200.0

    def test_categorias_ordenadas_por_nome(self, app_test, usuario_no_db):
        """Testa que categorias são retornadas ordenadas por nome."""
        with app_test.app_context():
            repo = SQLAlchemyCategoriaRepository()
            
            # Cria categorias em ordem aleatória
            c1 = Categoria(id=None, usuario_id=usuario_no_db.id, nome="Zebra", teto=100.0)
            c2 = Categoria(id=None, usuario_id=usuario_no_db.id, nome="Alimentação", teto=200.0)
            c3 = Categoria(id=None, usuario_id=usuario_no_db.id, nome="Maçã", teto=150.0)
            
            repo.salvar(c1)
            repo.salvar(c2)
            repo.salvar(c3)
            
            resultado = repo.buscar_por_usuario(usuario_no_db.id)
            
            # Verifica ordem alfabética
            nomes = [c.nome for c in resultado]
            assert nomes == ["Alimentação", "Maçã", "Zebra"]

    def test_categoria_sem_teto_permite_none(self, app_test, usuario_no_db):
        """Testa que categoria sem teto permite None."""
        with app_test.app_context():
            repo = SQLAlchemyCategoriaRepository()
            
            categoria = Categoria(
                id=None,
                usuario_id=usuario_no_db.id,
                nome="Diversos",
                teto=None
            )
            
            resultado = repo.salvar(categoria)
            
            assert resultado.teto is None
            db_cat = DBCategoria.query.filter_by(id=resultado.id).first()
            assert db_cat.teto is None
