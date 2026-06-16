from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import current_user, login_required
from datetime import datetime

from src.infrastructure.database.repositories import SQLAlchemyTransacaoRepository, SQLAlchemyCategoriaRepository
from src.application.finance_use_cases import AtualizarTetoCategoriaUseCase, CriarTransacaoUseCase, CriarCategoriaUseCase, DeletarTransacaoUseCase, EditarTransacaoUseCase, ListarCategoriasUseCase

financas_bp = Blueprint('financas', __name__)

categoria_repo = SQLAlchemyCategoriaRepository()
transacao_repo = SQLAlchemyTransacaoRepository()

criar_categoria_use_case = CriarCategoriaUseCase(categoria_repo)
listar_categorias_uc = ListarCategoriasUseCase(categoria_repo)
atualizar_teto_use_case = AtualizarTetoCategoriaUseCase(categoria_repo)

criar_tx_use_case = CriarTransacaoUseCase(transacao_repo)
deletar_tx_use_case = DeletarTransacaoUseCase(transacao_repo)
editar_tx_use_case = EditarTransacaoUseCase(transacao_repo)


@financas_bp.route('/transacao/nova/', methods=['POST'])
@login_required
def nova_transacao():
    try:
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


@financas_bp.route('/categoria/<int:categoria_id>/editar/', methods=['POST'])
@login_required
def editar_categoria(categoria_id):
    try:
        nome = request.form.get('nome')
        teto_raw = request.form.get('teto')
        teto = float(teto_raw) if teto_raw and teto_raw.strip() else None

        atualizar_teto_use_case.executar(
            categoria_id=categoria_id,
            usuario_id=current_user.id,
            nome=nome,
            teto=teto
        )
        flash("Teto da categoria atualizado com sucesso!")
    except ValueError as e:
        flash(str(e))
    except Exception:
        flash("Erro ao salvar alteração da categoria.")
        
    return redirect(url_for('contas.home'))

@financas_bp.route('/transacao/<int:transacao_id>/excluir/', methods=['POST'])
@login_required
def excluir_transacao(transacao_id):
    sucesso = deletar_tx_use_case.executar(transacao_id, current_user.id)
    if sucesso:
        flash("Transação excluída com sucesso!")
    else:
        flash("Erro ao excluir transação.")
    return redirect(url_for('contas.home'))

@financas_bp.route('/transacao/<int:transacao_id>/editar/', methods=['GET', 'POST'])
@login_required
def editar_transacao(transacao_id):
    transacao = transacao_repo.buscar_por_id(transacao_id, current_user.id)
    if not transacao:
        flash("Transação não encontrada.")
        return redirect(url_for('contas.home'))

    if request.method == 'POST':
        try:
            valor = float(request.form.get('valor', 0))
            tipo = request.form.get('tipo', 'SAIDA')
            categoria_raw = request.form.get('categoria')
            categoria_id = int(categoria_raw) if categoria_raw not in (None, '', 'None') else None
            
            data_str = request.form.get('data')
            data = datetime.strptime(data_str, '%Y-%m-%d').date() if data_str else datetime.now().date()
            descricao = request.form.get('descricao', '')

            editar_tx_use_case.executar(
                transacao_id=transacao_id,
                usuario_id=current_user.id,
                categoria_id=categoria_id,
                valor=valor,
                tipo=tipo,
                data=data,
                descricao=descricao
            )
            flash("Transação atualizada com sucesso!")
            return redirect(url_for('contas.home'))
        except ValueError as e:
            flash(str(e))

    categorias = listar_categorias_uc.executar(current_user.id)
    return render_template('financas/editar_transacao.html', transacao=transacao, categorias=categorias)