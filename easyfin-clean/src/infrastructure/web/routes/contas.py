from datetime import date, timedelta
from itertools import groupby
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


def _coletar_financas(usuario_id):
    """
    Monta os dados financeiros usado pelo dashbard e extrato
    """

    repo_tx = SQLAlchemyTransacaoRepository()
    transacoes = repo_tx.buscar_por_usuario(usuario_id)

    repo_cat=SQLAlchemyCategoriaRepository()
    categorias = ListarCategoriasUseCase(repo_cat).executar(usuario_id)
    categorias_map = {cat.id: cat.nome for cat in categorias}

    total_entradas = sum(t.valor for t in transacoes if t.tipo == 'ENTRADA')
    total_saidas = sum(t.valor for t in transacoes if t.tipo == 'SAIDA')
    saldo_total = total_entradas - total_saidas

    #Agrupa por dia - transação já vem ordenada (data desc)
    hoje = date.today()
    ontem = hoje - timedelta(days=1)
    grupos = []

    for dia, items, in groupby (transacoes, key=lambda t: t.data):
        if dia == hoje:
            rotulo = 'Hoje'
        elif dia == ontem:
            rotulo = "Ontem"
        else:
            rotulo = dia.strftime('%d/%m/%Y')
        grupos.append({'rotulo': rotulo, 'transacoes': list(items)})

    # Dict empacotado em dados e desempacotado em **dados
    return dict(
        categorias=categorias,
        categorias_map=categorias_map,
        grupos=grupos,
        saldo_total=saldo_total,
        total_entradas=total_entradas,
        total_saidas=total_saidas,
    )

@contas_bp.route('/dashboard/')
@login_required
def dashboard():
    dados = _coletar_financas(current_user.id)
    return render_template(
        'home.html',
        user=current_user,
        data_hoje=date.today().strftime('%Y-%m-%d'),
        **dados
    )

@contas_bp.route('/extrato/')
@login_required
def extrato():
    dados= _coletar_financas(current_user.id)
    return render_template('extrato.html', user=current_user, **dados)

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
