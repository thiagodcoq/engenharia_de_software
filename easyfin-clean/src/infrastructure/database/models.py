# src/infrastructure/database/models.py
from src.infrastructure.database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class DBUsuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, senha: str):
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<DBUsuario {self.email}>"


class DBCategoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)  # Armazena a referência do ID do usuário
    nome = db.Column(db.String(50), nullable=False)
    teto = db.Column(db.Numeric(10, 2), nullable=True)  # Limite opcional igual ao Django

    # Replica a restrição unique_together do Django (usuario_id + nome único)
    __table_args__ = (
        db.UniqueConstraint('usuario_id', 'nome', name='_usuario_categoria_uc'),
    )

    def __repr__(self):
        return f"<DBCategoria {self.nome}>"


class DBTransacao(db.Model):
    __tablename__ = 'transacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    
    # O ondelete='SET NULL' replica o comportamento on_delete=models.SET_NULL do Django
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id', ondelete='SET NULL'), nullable=True)
    
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    tipo = db.Column(db.String(7), default='SAIDA')
    data = db.Column(db.Date, nullable=False)
    criado_em = db.Column(db.DateTime, default=db.func.now())  # auto_now_add=True equivalente

    def __repr__(self):
        return f"<DBTransacao {self.descricao} - R$ {self.valor}>"