from src.infrastructure.database import db

class DBTransacao(db.Model):
    __tablename__ = 'transacoes'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    tipo = db.Column(db.String(7), default='SAIDA')
    data = db.Column(db.Date, nullable=False)