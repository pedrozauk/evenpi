from flask import url_for
from backend.utils.verificacoes import verifica_se_e_lista


def test_app_foi_criado(app):
    """testa se o aplicativo foi criado com a pasta correta"""
    assert app.name ==  'backend.app'



def test_endpoint_invalido_retorna_404(client):
    """testa se for passado um url errada retorna 404"""
    assert client.get('/sdadas').status_code == 404


    

def test_endpoint_evento_sem_autenticacao(client):
    assert client.get(url_for("evento.evento")).status_code == 401

def test_autenticacao_usuario_incorreto(user_autentication, preenche_banco):
    assert user_autentication(username= "admin", password="admin").status_code == 401

def test_autenticacao_usuario_correto(client, user_autentication,preenche_banco):
    assert  user_autentication("teste.user","12345").status_code == 200


def test_retorna_jwt_autenticacao(user_autentication,preenche_banco):
    username = "teste.user"
    password = "12345"
    assert user_autentication(username,password).status_code == 200
    assert user_autentication(username,password).json.get("acess_token", None) != None
    assert user_autentication(username,password).json.get("refresh_token", None) != None


def test_evento_endpoint_get(user_autentication, client,preenche_banco):
    username = "teste.user"
    password = "12345"
    response_login = user_autentication(username, password)
    acess_token = response_login.json.get("acess_token")
    headers =  {"Authorization": f"Bearer {acess_token}"}

    assert client.get(url_for("evento.evento"), headers=headers).status_code == 200
    lista_eventos = client.get(url_for("evento.evento"), headers=headers).json
    assert verifica_se_e_lista(lista_eventos)== True
    assert len(lista_eventos) > 2


def test_evento_endpoint_post(user_autentication,client):
    username = "admin"
    password = "1234"
    response_login = user_autentication(username, password)
    acess_token = response_login.json.get("acess_token")
    headers =  {"Authorization": f"Bearer {acess_token}"}
    pass