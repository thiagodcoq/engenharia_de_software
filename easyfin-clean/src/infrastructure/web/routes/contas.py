from datetime import date
from src.application.finance_use_cases import ListarCategoriasUseCase
from src.application.finance_use_cases import ListarCategoriasUseCase
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.infrastructure.database import db
from src.infrastructure.database.models import DBUsuario
from flask_login import login_user, logout_user, login_required, current_user

from src.infrastructure.database.repositories import SQLAlchemyTransacaoRepository, SQLAlchemyCategoriaRepository

contas_bp = Blueprint('contas', __name__)

@contas_bp.route('/')
def home():
    # A raiz é apenas um "porteiro": nunca renderiza tela própria.
    # Logado -> menu principal (dashboard); deslogado -> login.
    if current_user.is_authenticated:
        return redirect(url_for('contas.dashboard'))
    return redirect(url_for('contas.login'))


@contas_bp.route('/dashboard/')
@login_required
def dashboard():
    data_hoje = date.today().strftime('%Y-%m-%d')

    # Busca transações
    repo_tx = SQLAlchemyTransacaoRepository()
    transacoes = repo_tx.buscar_por_usuario(current_user.id)

    # Busca categorias através do Use Case
    repo_cat = SQLAlchemyCategoriaRepository()
    listar_categorias_uc = ListarCategoriasUseCase(repo_cat)
    categorias = listar_categorias_uc.executar(current_user.id)

    return render_template(
        'home.html',
        user=current_user,
        data_hoje=data_hoje,
        transacoes=transacoes,
        categorias=categorias
    )

@contas_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = DBUsuario.query.filter_by(email=email).first()
        if user and user.check_password(senha):
            login_user(user)
            flash('Login realizado com sucesso!')
            return redirect(url_for('contas.dashboard'))
        flash('Email ou senha inválidos')
    return render_template('contas/login.html')


@contas_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Desconectado com sucesso')
    return redirect(url_for('contas.home'))


@contas_bp.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if DBUsuario.query.filter_by(email=email).first():
            flash('Email já cadastrado')
            return redirect(url_for('contas.cadastro'))

        user = DBUsuario(nome=nome, email=email)
        user.set_password(senha)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Conta criada e usuário logado')
        return redirect(url_for('contas.dashboard'))

    return render_template('contas/cadastro.html')
