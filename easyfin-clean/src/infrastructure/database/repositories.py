from typing import List, Optional
from src.core.repositories import CategoriaRepositoryInterface, TransacaoRepositoryInterface
from src.core.entities import Transacao as DomainTransacao, Categoria as DomainCategoria

from src.infrastructure.database.models import DBTransacao, DBCategoria
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
    
    def buscar_todas_por_usuario(self, usuario_id: int) -> List[DomainTransacao]:
        db_txs = DBTransacao.query.filter_by(usuario_id=usuario_id).all()
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

    def buscar_por_id(self, transacao_id: int, usuario_id: int) -> Optional[DomainTransacao]:
        db_tx = DBTransacao.query.filter_by(id=transacao_id, usuario_id=usuario_id).first()
        if db_tx:
            return DomainTransacao(
                id=db_tx.id,
                usuario_id=db_tx.usuario_id,
                categoria_id=db_tx.categoria_id,
                descricao=db_tx.descricao,
                valor=float(db_tx.valor),
                tipo=db_tx.tipo,
                data=db_tx.data
            )
        return None

    def deletar(self, transacao_id: int, usuario_id: int) -> bool:
        db_tx = DBTransacao.query.filter_by(id=transacao_id, usuario_id=usuario_id).first()
        
        if db_tx:
            db.session.delete(db_tx)
            db.session.commit()
            return True
        return False
    
    def buscar_por_periodo(self, usuario_id, inicio, fim):
        db_txs = DBTransacao.query.filter(
            DBTransacao.usuario_id == usuario_id,
            DBTransacao.data >= inicio,
            DBTransacao.data < fim,
        ).order_by(DBTransacao.data.desc()).all()

        return [
            DomainTransacao(
            id=tx.id,
            usuario_id=tx.usuario_id,
            categoria_id=tx.categoria_id,
            descricao=tx.descricao,
            valor=float(tx.valor),
            tipo=tx.tipo,
            data=tx.data,
        ) for tx in db_txs
        ]
    
class SQLAlchemyCategoriaRepository(CategoriaRepositoryInterface):
    def buscar_por_usuario(self, usuario_id: int) -> List[DomainCategoria]:
        db_categorias = DBCategoria.query.filter_by(usuario_id=usuario_id).order_by(DBCategoria.nome).all()
        
        return [
            DomainCategoria(
                id=cat.id,
                usuario_id=cat.usuario_id,
                nome=cat.nome,
                teto=float(cat.teto) if cat.teto else None
            ) for cat in db_categorias
        ]
    
    def buscar_por_id(self, categoria_id, usuario_id):
        cat = DBCategoria.query.filter_by(id=categoria_id, usuario_id=usuario_id).first()
        if not cat:
            return None
        return DomainCategoria(
            id=cat.id,
            usuario_id=cat.usuario_id,
            nome=cat.nome,
            teto=float(cat.teto) if cat.teto else None,
        )
    
    def salvar(self, categoria: DomainCategoria) -> DomainCategoria:
        if categoria.id:
            db_cat = DBCategoria.query.filter_by(id=categoria.id, usuario_id=categoria.usuario_id).first()
            if db_cat:
                db_cat.nome = categoria.nome
                db_cat.teto = categoria.teto
        else:
            db_cat = DBCategoria(
                usuario_id=categoria.usuario_id,
                nome=categoria.nome,
                teto=categoria.teto
            )
            db.session.add(db_cat)
            
        db.session.commit()
        categoria.id = db_cat.id
        return categoria