from flask import Blueprint, request, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime

from src.infrastructure.database.repositories import SQLAlchemyTransacaoRepository, SQLAlchemyCategoriaRepository
from src.application.finance_use_cases import CriarTransacaoUseCase, CriarCategoriaUseCase

financas_bp = Blueprint('financas', __name__)

transacao_repo = SQLAlchemyTransacaoRepository()
criar_tx_use_case = CriarTransacaoUseCase(transacao_repo)

categoria_repo = SQLAlchemyCategoriaRepository()
criar_categoria_use_case = CriarCategoriaUseCase(categoria_repo)



@financas_bp.route('/transacao/nova/', methods=['POST'])
@login_required
def nova_transacao():
    try:
        # Extrai os dados enviados pelo formulário HTML original
        valor = float(request.form.get('valor', 0))
        tipo = request.form.get('tipo', 'SAIDA')

        categoria_raw = request.form.get('categoria')
        categoria_id = int(categoria_raw) if categoria_raw not in (None, '', 'None') else None

        data_str = request.form.get('data')
        if data_str:
            data = datetime.strptime(data_str, '%Y-%m-%d').date()
        else:
            data = datetime.now().date()

        descricao = request.form.get('descricao', '')

        # Executa a regra de negócio através do Caso de Uso
        criar_tx_use_case.executar(
            usuario_id=current_user.id,
            categoria_id=categoria_id,
            valor=valor,
            tipo=tipo,
            data=data,
            descricao=descricao
        )
        flash("Transação salva com sucesso!")
    except ValueError as e:
        flash(str(e))
        
    return redirect(url_for('contas.home'))


@financas_bp.route('/categoria/nova/', methods=['POST'])
@login_required
def nova_categoria():
    try:
        nome = request.form.get('nome')
        teto_raw = request.form.get('teto')
        teto = float(teto_raw) if teto_raw and teto_raw.strip() else None

        criar_categoria_use_case.executar(
            usuario_id=current_user.id,
            nome=nome,
            teto=teto
        )
        flash("Categoria adicionada com sucesso!")
    except ValueError as e:
        flash(str(e))
    except Exception:
        # Tratamento caso o banco de dados barre a constraint unique(usuario_id, nome)
        flash("Erro ao salvar categoria. Certifique-se de que o nome já não existe.")
        
    return redirect(url_for('contas.home'))