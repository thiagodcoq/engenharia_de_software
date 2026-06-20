"""Testes unitários para casos de uso (use cases) de finanças."""

import pytest
from datetime import date
from src.application.finance_use_cases import (
    CriarTransacaoUseCase,
    ListarCategoriasUseCase,
    CriarCategoriaUseCase
)
from src.core.entities import Transacao, Categoria


class TestCriarTransacaoUseCase:
    """Testes para o caso de uso: Criar Transação."""

    def test_criar_transacao_valida(self, mock_transacao_repo, usuario_fixture, categoria_fixture):
        """Testa criação bem-sucedida de uma transação com dados válidos."""
        use_case = CriarTransacaoUseCase(mock_transacao_repo)

        resultado = use_case.executar(
            usuario_id=usuario_fixture.id,
            categoria_id=categoria_fixture.id,
            valor=100.0,
            tipo="SAIDA",
            data=date.today(),
            descricao="Teste transação"
        )

        assert resultado is not None
        assert resultado.id is not None
        assert resultado.usuario_id == usuario_fixture.id
        assert resultado.valor == 100.0
        assert resultado.tipo == "SAIDA"

    def test_criar_transacao_valor_invalido_zero(self, mock_transacao_repo, usuario_fixture):
        """Testa rejeição de transação com valor zero."""
        use_case = CriarTransacaoUseCase(mock_transacao_repo)

        with pytest.raises(ValueError, match="Valor deve ser maior que zero"):
            use_case.executar(
                usuario_id=usuario_fixture.id,
                categoria_id=1,
                valor=0,
                tipo="SAIDA",
                data=date.today(),
                descricao="Inválido"
            )

    def test_criar_transacao_valor_negativo(self, mock_transacao_repo, usuario_fixture):
        """Testa rejeição de transação com valor negativo."""
        use_case = CriarTransacaoUseCase(mock_transacao_repo)

        with pytest.raises(ValueError, match="Valor deve ser maior que zero"):
            use_case.executar(
                usuario_id=usuario_fixture.id,
                categoria_id=1,
                valor=-50.0,
                tipo="ENTRADA",
                data=date.today(),
                descricao="Inválido"
            )

    def test_criar_transacao_sem_descricao_usa_padrao(self, mock_transacao_repo, usuario_fixture):
        """Testa que transação sem descrição recebe descrição padrão."""
        use_case = CriarTransacaoUseCase(mock_transacao_repo)

        resultado = use_case.executar(
            usuario_id=usuario_fixture.id,
            categoria_id=None,
            valor=50.0,
            tipo="ENTRADA",
            data=date.today(),
            descricao=""
        )

        assert resultado.descricao == "Transação"

    def test_criar_transacao_categoria_opcional(self, mock_transacao_repo, usuario_fixture):
        """Testa criação de transação sem categoria."""
        use_case = CriarTransacaoUseCase(mock_transacao_repo)

        resultado = use_case.executar(
            usuario_id=usuario_fixture.id,
            categoria_id=None,
            valor=75.0,
            tipo="SAIDA",
            data=date.today(),
            descricao="Transação sem categoria"
        )

        assert resultado.categoria_id is None


class TestListarCategoriasUseCase:
    """Testes para o caso de uso: Listar Categorias."""

    def test_listar_categorias_vazio(self, mock_categoria_repo, usuario_fixture):
        """Testa listagem de categorias quando não há nenhuma."""
        use_case = ListarCategoriasUseCase(mock_categoria_repo)

        resultado = use_case.executar(usuario_fixture.id)

        assert resultado == []

    def test_listar_categorias_do_usuario(self, mock_categoria_repo, usuario_fixture):
        """Testa listagem de categorias apenas do usuário especificado."""
        use_case = ListarCategoriasUseCase(mock_categoria_repo)

        # Salva categorias para o usuário 1
        cat1 = Categoria(id=None, usuario_id=1, nome="Alimentação", teto=500.0)
        cat2 = Categoria(id=None, usuario_id=1, nome="Transporte", teto=200.0)
        mock_categoria_repo.salvar(cat1)
        mock_categoria_repo.salvar(cat2)

        # Salva categoria para o usuário 2 (não deve aparecer)
        cat3 = Categoria(id=None, usuario_id=2, nome="Saúde", teto=300.0)
        mock_categoria_repo.salvar(cat3)

        resultado = use_case.executar(usuario_id=1)

        assert len(resultado) == 2
        assert all(cat.usuario_id == 1 for cat in resultado)


class TestCriarCategoriaUseCase:
    """Testes para o caso de uso: Criar Categoria."""

    def test_criar_categoria_valida(self, mock_categoria_repo, usuario_fixture):
        """Testa criação bem-sucedida de uma categoria."""
        use_case = CriarCategoriaUseCase(mock_categoria_repo)

        resultado = use_case.executar(
            usuario_id=usuario_fixture.id,
            nome="Lazer",
            teto=150.0
        )

        assert resultado is not None
        assert resultado.id is not None
        assert resultado.nome == "Lazer"
        assert resultado.teto == 150.0
        assert resultado.usuario_id == usuario_fixture.id

    def test_criar_categoria_sem_teto(self, mock_categoria_repo, usuario_fixture):
        """Testa criação de categoria sem teto (opcional)."""
        use_case = CriarCategoriaUseCase(mock_categoria_repo)

        resultado = use_case.executar(
            usuario_id=usuario_fixture.id,
            nome="Diversos",
            teto=None
        )

        assert resultado.teto is None

    def test_criar_categoria_nome_vazio_rejeita(self, mock_categoria_repo, usuario_fixture):
        """Testa rejeição de categoria com nome vazio."""
        use_case = CriarCategoriaUseCase(mock_categoria_repo)

        with pytest.raises(ValueError, match="O nome da categoria não pode ser vazio"):
            use_case.executar(
                usuario_id=usuario_fixture.id,
                nome="",
                teto=100.0
            )

    def test_criar_categoria_nome_whitespace_rejeita(self, mock_categoria_repo, usuario_fixture):
        """Testa rejeição de categoria com nome contendo apenas espaços."""
        use_case = CriarCategoriaUseCase(mock_categoria_repo)

        with pytest.raises(ValueError, match="O nome da categoria não pode ser vazio"):
            use_case.executar(
                usuario_id=usuario_fixture.id,
                nome="   ",
                teto=100.0
            )

    def test_criar_categoria_teto_negativo_rejeita(self, mock_categoria_repo, usuario_fixture):
        """Testa rejeição de categoria com teto negativo."""
        use_case = CriarCategoriaUseCase(mock_categoria_repo)

        with pytest.raises(ValueError, match="O teto de gastos não pode ser um valor negativo"):
            use_case.executar(
                usuario_id=usuario_fixture.id,
                nome="Teste",
                teto=-100.0
            )

    def test_criar_categoria_teto_zero_aceita(self, mock_categoria_repo, usuario_fixture):
        """Testa aceitação de categoria com teto zero."""
        use_case = CriarCategoriaUseCase(mock_categoria_repo)

        resultado = use_case.executar(
            usuario_id=usuario_fixture.id,
            nome="Sem gastos",
            teto=0.0
        )

        assert resultado.teto == 0.0

    def test_criar_categoria_nome_com_espacos_e_normalizado(self, mock_categoria_repo, usuario_fixture):
        """Testa que nome com espaços é normalizado."""
        use_case = CriarCategoriaUseCase(mock_categoria_repo)

        resultado = use_case.executar(
            usuario_id=usuario_fixture.id,
            nome="  Educação  ",
            teto=200.0
        )

        assert resultado.nome == "Educação"
