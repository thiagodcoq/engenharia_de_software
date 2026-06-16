from datetime import date
from src.core.entities import Transacao
from src.core.repositories import TransacaoRepositoryInterface

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