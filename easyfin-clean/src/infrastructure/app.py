import os
from flask import Flask
from src.infrastructure.database import db
from src.infrastructure.web.routes.financas import financas_bp

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'easyfin-secret-key-dev')
    
    # Se houver DATABASE_URL (produção/Vercel), usa PostgreSQL, senão SQLite local
    database_url = os.environ.get("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o banco com o app Flask
    db.init_app(app)

    # Substitui o "migrate" criando as tabelas automaticamente se não existirem
    with app.app_context():
        # Importar os modelos garante que o SQLAlchemy os reconheça antes de criar as tabelas
        from src.infrastructure.database.models import DBTransacao 
        db.create_all()

    # Registra as rotas (Blueprints)
    app.register_blueprint(financas_bp)
    # app.register_blueprint(contas_bp)

    return app