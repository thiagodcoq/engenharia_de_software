# src/infrastructure/web/app.py
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
    
    database_url = os.environ.get("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # ALTERAÇÃO AQUI: Importa o arquivo de modelos inteiro para registrar 'categorias' e 'transacoes'
        from src.infrastructure.database import models
        db.create_all()

    app.register_blueprint(financas_bp)

    return app