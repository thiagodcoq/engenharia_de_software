# src/infrastructure/database/repositories.py
from typing import List
from src.core.repositories import TransacaoRepositoryInterface
from src.core.entities import Transacao as DomainTransacao
from src.infrastructure.database.models import DBTransacao
from src.infrastructure.database import db

class SQLAlchemyTransacaoRepository(TransacaoRepositoryInterface):
    
    def salvar(self, transacao: DomainTransacao) -> DomainTransacao:
        if transacao.id:
            db_tx = DBTransacao.query.filter_by(id=transacao.id, usuario_id=transacao.usuario_id).first()
            if db_tx:
                db_tx.descricao = transacao.descricao
                db_tx.valor = transacao.valor
                db_tx.tipo = transacao.tipo
                db_tx.data = transacao.data
                db_tx.categoria_id = transacao.categoria_id
        else:
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

    def buscar_por_usuario(self, usuario_id: int, limite: int = 20) -> List[DomainTransacao]:
        db_txs = DBTransacao.query.filter_by(usuario_id=usuario_id)\
            .order_by(DBTransacao.data.desc(), DBTransacao.id.desc())\
            .limit(limite)\
            .all()
            
        return [
            DomainTransacao(
                id=tx.id,
                usuario_id=tx.usuario_id,
                categoria_id=tx.categoria_id,
                descricao=tx.descricao,
                valor=float(tx.valor),
                tipo=tx.tipo,
                data=tx.data
            ) for tx in db_txs
        ]

    def deletar(self, transacao_id: int, usuario_id: int) -> bool:
        db_tx = DBTransacao.query.filter_by(id=transacao_id, usuario_id=usuario_id).first()
        
        if db_tx:
            db.session.delete(db_tx)
            db.session.commit()
            return True
        return False