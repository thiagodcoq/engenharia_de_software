from datetime import date
from typing import List, Optional
from src.core.entities import Categoria, CategoriaSaldoDTO, Transacao
from src.core.repositories import CategoriaRepositoryInterface, TransacaoRepositoryInterface

class CriarTransacaoUseCase:
    def __init__(self, transacao_repo: TransacaoRepositoryInterface):
        self.transacao_repo = transacao_repo

    def executar(self, usuario_id: int, categoria_id: Optional[int], valor: float, tipo: str, data: date, descricao: str):
        if valor <= 0:
            raise ValueError("Valor deve ser maior que zero")
            
        if tipo == 'SAIDA' and not categoria_id:
            raise ValueError("A categoria é obrigatória para o registro de uma despesa (SAIDA).")
        
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
    
class DeletarTransacaoUseCase:
    def __init__(self, transacao_repo: TransacaoRepositoryInterface):
        self.transacao_repo = transacao_repo

    def executar(self, transacao_id: int, usuario_id: int) -> bool:
        return self.transacao_repo.deletar(transacao_id, usuario_id)

class EditarTransacaoUseCase:
    def __init__(self, transacao_repo: TransacaoRepositoryInterface):
        self.transacao_repo = transacao_repo

    def executar(self, transacao_id: int, usuario_id: int, categoria_id: Optional[int], valor: float, tipo: str, data: date, descricao: str):
        if valor <= 0:
            raise ValueError("Valor deve ser maior que zero")
            
        if tipo == 'SAIDA' and not categoria_id:
            raise ValueError("A categoria é obrigatória para o registro de uma despesa (SAIDA).")
        
        if not descricao:
            descricao = "Transação"

        transacao_atualizada = Transacao(
            id=transacao_id,
            usuario_id=usuario_id,
            categoria_id=categoria_id,
            descricao=descricao,
            valor=valor,
            tipo=tipo,
            data=data
        )
        return self.transacao_repo.salvar(transacao_atualizada)

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

class ObterSaldoCategoriasUseCase:
    def __init__(self, categoria_repo: CategoriaRepositoryInterface, transacao_repo: TransacaoRepositoryInterface):
        self.categoria_repo = categoria_repo
        self.transacao_repo = transacao_repo

    def executar(self, usuario_id: int) -> List[CategoriaSaldoDTO]:
        categorias = self.categoria_repo.buscar_por_usuario(usuario_id)
        transacoes = self.transacao_repo.buscar_todas_por_usuario(usuario_id)
        
        gastos_por_categoria = {}
        for tx in transacoes:
            if tx.tipo == "SAIDA" and tx.categoria_id is not None:
                gastos_por_categoria[tx.categoria_id] = gastos_por_categoria.get(tx.categoria_id, 0.0) + tx.valor
        
        resultado = []
        for cat in categorias:
            gastos = gastos_por_categoria.get(cat.id, 0.0)
            disponivel = (cat.teto - gastos) if cat.teto is not None else None
            resultado.append(CategoriaSaldoDTO(
                id=cat.id,
                nome=cat.nome,
                teto=cat.teto,
                gastos=gastos,
                disponivel=disponivel
            ))
        return resultado
    
class AtualizarTetoCategoriaUseCase:
    def __init__(self, categoria_repo: CategoriaRepositoryInterface):
        self.categoria_repo = categoria_repo

    def executar(self, categoria_id: int, usuario_id: int, nome: str, teto: Optional[float] = None) -> Categoria:
        if not nome or not nome.strip():
            raise ValueError("O nome da categoria não pode ser vazio.")
        
        if teto is not None and teto < 0:
            raise ValueError("O teto de gastos não pode ser um valor negativo.")
            
        categoria_atualizada = Categoria(
            id=categoria_id,
            usuario_id=usuario_id,
            nome=nome.strip(),
            teto=teto
        )
        return self.categoria_repo.salvar(categoria_atualizada)