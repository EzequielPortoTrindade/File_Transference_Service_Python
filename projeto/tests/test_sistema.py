import os
import socket
import threading
import time

import pytest

from server import (
    iniciar_servidor,
    SERVER_FILES,
)

HOST = "localhost"
PORT = 5050
BUFFER_SIZE = 1024


@pytest.fixture(scope="session", autouse=True)
def servidor():
    """
    Inicia o servidor uma vez para toda a suíte.
    """

    thread = threading.Thread(
        target=iniciar_servidor,
        daemon=True
    )

    thread.start()

    time.sleep(1)

    yield


@pytest.fixture(autouse=True)
def limpar_arquivos():
    """
    Limpa os arquivos do servidor antes e depois de cada teste.
    """

    os.makedirs(SERVER_FILES, exist_ok=True)

    for arquivo in os.listdir(SERVER_FILES):
        caminho = os.path.join(SERVER_FILES, arquivo)

        if os.path.isfile(caminho):
            os.remove(caminho)

    yield

    for arquivo in os.listdir(SERVER_FILES):
        caminho = os.path.join(SERVER_FILES, arquivo)

        if os.path.isfile(caminho):
            os.remove(caminho)


def criar_cliente():
    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client.connect((HOST, PORT))

    return client


def test_upload_e_listagem():
    """
    Fluxo:
    1. Faz upload de um arquivo.
    2. Lista arquivos.
    3. Verifica se o arquivo aparece.
    """

    client = criar_cliente()

    nome_arquivo = "teste.txt"
    conteudo = b"arquivo de teste"

    comando = f"UPLOAD|{nome_arquivo}|{len(conteudo)}"

    client.sendall(comando.encode())

    time.sleep(0.1)

    client.sendall(conteudo)

    time.sleep(0.3)

    client.sendall(b"LISTAR")

    resposta = client.recv(BUFFER_SIZE).decode()

    assert nome_arquivo in resposta

    caminho = os.path.join(
        SERVER_FILES,
        nome_arquivo
    )

    assert os.path.exists(caminho)

    with open(caminho, "rb") as f:
        assert f.read() == conteudo

    client.sendall(b"SAIR")

    client.close()


def test_download_arquivo():
    """
    Fluxo:
    1. Cria arquivo no servidor.
    2. Solicita download.
    3. Verifica conteúdo recebido.
    """

    nome_arquivo = "download.txt"

    conteudo_original = (
        b"conteudo enviado pelo servidor"
    )

    caminho = os.path.join(
        SERVER_FILES,
        nome_arquivo
    )

    with open(caminho, "wb") as f:
        f.write(conteudo_original)

    client = criar_cliente()

    comando = f"DOWNLOAD|{nome_arquivo}"

    client.sendall(comando.encode())

    resposta = client.recv(BUFFER_SIZE).decode()

    status, tamanho = resposta.split("|")

    assert status == "OK"

    tamanho = int(tamanho)

    assert tamanho == len(conteudo_original)

    client.sendall(b"READY")

    recebido = b""

    while len(recebido) < tamanho:
        chunk = client.recv(BUFFER_SIZE)

        if not chunk:
            break

        recebido += chunk

    assert recebido == conteudo_original

    client.sendall(b"SAIR")

    client.close()
