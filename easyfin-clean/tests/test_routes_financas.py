import pytest
from datetime import date
from src.infrastructure.database.models import DBCategoria, DBTransacao
from src.infrastructure.database import db

def test_nova_transacao_success(app_test, usuario_no_db, categoria_no_db):
    client = app_test.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(usuario_no_db.id)
        
    response = client.post('/transacao/nova/', data={
        'valor': '150.50',
        'tipo': 'SAIDA',
        'categoria': str(categoria_no_db.id),
        'data': '2023-10-15',
        'descricao': 'Compra'
    })
    
    assert response.status_code == 302
    assert '/' in response.location
    
    with app_test.app_context():
        tx = DBTransacao.query.filter_by(usuario_id=usuario_no_db.id).first()
        assert tx is not None
        assert tx.valor == 150.50

def test_nova_transacao_error(app_test, usuario_no_db):
    client = app_test.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(usuario_no_db.id)
        
    response = client.post('/transacao/nova/', data={
        'valor': '-50.00', # error
        'tipo': 'SAIDA',
        'descricao': 'Compra'
    })
    
    assert response.status_code == 302

def test_nova_categoria_success(app_test, usuario_no_db):
    client = app_test.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(usuario_no_db.id)
        
    response = client.post('/categoria/nova/', data={
        'nome': 'Nova Categoria',
        'teto': '1000'
    })
    
    assert response.status_code == 302
    with app_test.app_context():
        cat = DBCategoria.query.filter_by(nome='Nova Categoria', usuario_id=usuario_no_db.id).first()
        assert cat is not None
        assert cat.teto == 1000.0

def test_nova_categoria_error(app_test, usuario_no_db):
    client = app_test.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(usuario_no_db.id)
        
    response = client.post('/categoria/nova/', data={
        'nome': '', # error
        'teto': '1000'
    })
    assert response.status_code == 302

def test_salvar_limite_success(app_test, usuario_no_db, categoria_no_db):
    client = app_test.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(usuario_no_db.id)
        
    response = client.post(f'/categoria/{categoria_no_db.id}/limite/', data={
        'teto': '2000'
    })
    assert response.status_code == 302
    assert '/orcamento' in response.location
    
    with app_test.app_context():
        cat = DBCategoria.query.get(categoria_no_db.id)
        assert cat.teto == 2000.0

def test_salvar_limite_negativo(app_test, usuario_no_db, categoria_no_db):
    client = app_test.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(usuario_no_db.id)
        
    response = client.post(f'/categoria/{categoria_no_db.id}/limite/', data={
        'teto': '-100'
    })
    assert response.status_code == 302

def test_salvar_limite_categoria_nao_encontrada(app_test, usuario_no_db):
    client = app_test.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(usuario_no_db.id)
        
    response = client.post(f'/categoria/9999/limite/', data={
        'teto': '100'
    })
    assert response.status_code == 302
