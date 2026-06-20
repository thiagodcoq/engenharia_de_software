from datetime import date
from typing import List, Optional
from src.core.entities import Categoria, Transacao
from src.core.repositories import CategoriaRepositoryInterface, TransacaoRepositoryInterface

class CriarTransacaoUseCase:
    def __init__(self, transacao_repo: TransacaoRepositoryInterface):
        self.transacao_repo = transacao_repo

    def executar(self, usuario_id: int, categoria_id: int, valor: float, tipo: str, data: date, descricao: str):
        if valor <= 0:
            raise ValueError("Valor deve ser maior que zero")
        
        # Regra de negócio herdada do formulário Django: se não houver descrição, usa o nome da categoria ou padrão
        if not descricao:
            descricao = "Transação"

        nova_tx = Transacao(
            id=None,
            usuario_id=usuario_id,
            categoria_id=categoria_id,
            descricao=descricao,
            valor=valor,
            tipo=tipo,
            data=data
        )
        return self.transacao_repo.salvar(nova_tx)

class ListarCategoriasUseCase:
    def __init__(self, categoria_repo: CategoriaRepositoryInterface):
        self.categoria_repo = categoria_repo

    def executar(self, usuario_id: int) -> List[Categoria]:
        return self.categoria_repo.buscar_por_usuario(usuario_id)
    

class CriarCategoriaUseCase:
    def __init__(self, categoria_repo: CategoriaRepositoryInterface):
        self.categoria_repo = categoria_repo

    def executar(self, usuario_id: int, nome: str, teto: Optional[float] = None) -> Categoria:
        if not nome or not nome.strip():
            raise ValueError("O nome da categoria não pode ser vazio.")
        
        if teto is not None and teto < 0:
            raise ValueError("O teto de gastos não pode ser um valor negativo.")
            
        nova_categoria = Categoria(
            id=None,
            usuario_id=usuario_id,
            nome=nome.strip(),
            teto=teto
        )
        return self.categoria_repo.salvar(nova_categoria)