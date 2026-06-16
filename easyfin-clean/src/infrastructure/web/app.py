# src/infrastructure/web/app.py
import os
from flask import Flask
from flask_login import LoginManager
from src.infrastructure.database import db
from src.infrastructure.web.routes.financas import financas_bp
from src.infrastructure.web.routes.contas import contas_bp

login_manager = LoginManager()


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
    login_manager.init_app(app)
    login_manager.login_view = 'contas.login'

    with app.app_context():
        # Importa modelos para registrar tabelas (DBUsuario, categorias e transacoes)
        from src.infrastructure.database import models

        @login_manager.user_loader
        def load_user(user_id):
            try:
                return models.DBUsuario.query.get(int(user_id))
            except Exception:
                return None

        db.create_all()

    # Registrar blueprints
    app.register_blueprint(contas_bp)
    app.register_blueprint(financas_bp)

    return app