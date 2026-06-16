from datetime import date # <-- 1. Adicione este import lá no topo
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.infrastructure.database import db
from src.infrastructure.database.models import DBUsuario
from flask_login import login_user, logout_user, login_required, current_user

contas_bp = Blueprint('contas', __name__)

@contas_bp.route('/')
def home():
    # 2. Capture a data de hoje formatada
    data_hoje = date.today().strftime('%Y-%m-%d')
    
    # 3. Envie a variável data_hoje para o seu template junto com o user
    return render_template('home.html', user=current_user, data_hoje=data_hoje)


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
