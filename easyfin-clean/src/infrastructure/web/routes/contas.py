from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.infrastructure.database import db
from src.infrastructure.database.models import DBUsuario
from flask_login import login_user, logout_user, login_required, current_user

from src.infrastructure.database.repositories import SQLAlchemyTransacaoRepository, SQLAlchemyCategoriaRepository
from src.application.finance_use_cases import ObterSaldoCategoriasUseCase, CalcularSaldoTotalMesUseCase

contas_bp = Blueprint('contas', __name__)

@contas_bp.route('/')
def home():
    data_hoje = date.today().strftime('%Y-%m-%d')
    transacoes = []
    categorias_saldo = []
    saldo_geral = None
    
    if current_user.is_authenticated:
        repo_tx = SQLAlchemyTransacaoRepository()
        transacoes = repo_tx.buscar_por_usuario(current_user.id)
        
        repo_cat = SQLAlchemyCategoriaRepository()
        obter_saldo_uc = ObterSaldoCategoriasUseCase(repo_cat, repo_tx)
        categorias_saldo = obter_saldo_uc.executar(current_user.id)
        
        calcular_saldo_uc = CalcularSaldoTotalMesUseCase(repo_tx)
        saldo_geral = calcular_saldo_uc.executar(current_user.id)
        
    return render_template(
        'home.html', 
        user=current_user, 
        data_hoje=data_hoje, 
        transacoes=transacoes,
        categorias=categorias_saldo,
        saldo_geral=saldo_geral
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
            return redirect(url_for('contas.home'))
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
        return redirect(url_for('contas.home'))

    return render_template('contas/cadastro.html')
