import pytest
from flask import url_for

def test_home_redirects_to_login_if_unauthenticated(app_test):
    client = app_test.test_client()
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.location

def test_home_redirects_to_dashboard_if_authenticated(app_test, usuario_no_db):
    client = app_test.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(usuario_no_db.id)
        sess['_fresh'] = True

    response = client.get('/')
    assert response.status_code == 302
    assert '/dashboard' in response.location

def test_dashboard_requires_login(app_test):
    client = app_test.test_client()
    response = client.get('/dashboard/')
    assert response.status_code == 302
    assert '/login' in response.location

def test_dashboard_authenticated(app_test, usuario_no_db):
    client = app_test.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(usuario_no_db.id)
    response = client.get('/dashboard/')
    assert response.status_code == 200

def test_extrato_authenticated(app_test, usuario_no_db):
    client = app_test.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(usuario_no_db.id)
    response = client.get('/extrato/')
    assert response.status_code == 200

def test_orcamento_authenticated(app_test, usuario_no_db, categoria_no_db):
    client = app_test.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(usuario_no_db.id)
    response = client.get('/orcamento/')
    assert response.status_code == 200

def test_perfil_authenticated(app_test, usuario_no_db):
    client = app_test.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(usuario_no_db.id)
    response = client.get('/perfil/')
    assert response.status_code == 200

def test_login_get(app_test):
    client = app_test.test_client()
    response = client.get('/login/')
    assert response.status_code == 200

def test_login_post_success(app_test, usuario_no_db):
    client = app_test.test_client()
    response = client.post('/login/', data={'email': 'joao@test.com', 'senha': 'senha123'})
    assert response.status_code == 302
    assert '/dashboard' in response.location

def test_login_post_failure(app_test, usuario_no_db):
    client = app_test.test_client()
    response = client.post('/login/', data={'email': 'joao@test.com', 'senha': 'wrongpassword'})
    assert response.status_code == 200 

def test_logout(app_test, usuario_no_db):
    client = app_test.test_client()
    with client.session_transaction() as sess:
        sess['_user_id'] = str(usuario_no_db.id)
    response = client.get('/logout/')
    assert response.status_code == 302
    assert '/' in response.location

def test_cadastro_get(app_test):
    client = app_test.test_client()
    response = client.get('/cadastro/')
    assert response.status_code == 200

def test_cadastro_post_success(app_test):
    client = app_test.test_client()
    response = client.post('/cadastro/', data={'nome': 'Novo User', 'email': 'novo@test.com', 'senha': '123'})
    assert response.status_code == 302
    assert '/dashboard' in response.location

def test_cadastro_post_existing_email(app_test, usuario_no_db):
    client = app_test.test_client()
    response = client.post('/cadastro/', data={'nome': 'Outro User', 'email': 'joao@test.com', 'senha': '123'})
    assert response.status_code == 302
    assert '/cadastro' in response.location
