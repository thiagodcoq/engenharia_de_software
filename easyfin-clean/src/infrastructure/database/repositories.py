from src.domain.repositories import TransacaoRepositoryInterface
from src.domain.entities import Transacao as DomainTransacao
from src.infrastructure.database.models import DBTransacao
from src.infrastructure.database import db

class SQLAlchemyTransacaoRepository(TransacaoRepositoryInterface):
    def salvar(self, transacao: DomainTransacao) -> DomainTransacao:
        db_tx = DBTransacao(
            usuario_id=transacao.usuario_id,
            categoria_id=transacao.categoria_id,
            descricao=transacao.descricao,
            valor=transacao.valor,
            tipo=transacao.tipo,
            data=transacao.data
        )
        db.session.add(db_tx)
        db.session.commit()
        transacao.id = db_tx.id
        return transacao