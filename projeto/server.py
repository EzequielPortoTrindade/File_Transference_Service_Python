"""
Servidor TCP para transferência de arquivos.
Gerencia uploads, downloads, listagem e remoção de arquivos.
"""

import socket
import threading
import os
from pathlib import Path

HOST = "localhost"
PORT = 5050
BUFFER_SIZE = 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_FILES = os.path.join(BASE_DIR, "server_files")

os.makedirs(SERVER_FILES, exist_ok=True)


def receber_arquivo(conn, nome_arquivo, tamanho):
    """Recebe arquivo enviado por um cliente."""

    nome_arquivo = os.path.basename(nome_arquivo)
    caminho = os.path.join(SERVER_FILES, nome_arquivo)

    with open(caminho, "wb") as f:
        bytes_recebidos = 0

        while bytes_recebidos < tamanho:
            dados = conn.recv(min(BUFFER_SIZE, tamanho - bytes_recebidos))

            if not dados:
                break

            f.write(dados)
            bytes_recebidos += len(dados)

    print(f"Arquivo recebido: {nome_arquivo}")


def enviar_arquivo(conn, nome_arquivo):
    """Envia arquivo solicitado pelo cliente."""

    nome_arquivo = os.path.basename(nome_arquivo)
    caminho = os.path.join(SERVER_FILES, nome_arquivo)

    if not os.path.exists(caminho):
        conn.sendall("ERRO".encode())
        return

    tamanho = os.path.getsize(caminho)

    conn.sendall(f"OK|{tamanho}".encode())

    resposta = conn.recv(BUFFER_SIZE).decode()

    if resposta != "READY":
        return

    with open(caminho, "rb") as f:
        while chunk := f.read(BUFFER_SIZE):
            conn.sendall(chunk)

    print(f"Arquivo enviado: {nome_arquivo}")


def listar_arquivos(conn):
    """Lista arquivos armazenados no servidor."""

    arquivos = os.listdir(SERVER_FILES)

    if not arquivos:
        conn.sendall("VAZIO".encode())
        return

    conn.sendall("\n".join(arquivos).encode())


def remover_arquivo(conn, nome_arquivo):
    """Remove arquivo com proteção contra path traversal."""

    base_dir = Path(SERVER_FILES).resolve()
    nome_arquivo_limpo = Path(nome_arquivo).name
    caminho = (base_dir / nome_arquivo_limpo).resolve()

    if base_dir != caminho.parent:
        conn.sendall("ERRO".encode())
        return

    if caminho.exists():
        caminho.unlink()
        conn.sendall("OK".encode())
        print(f"Arquivo removido: {nome_arquivo_limpo}")
    else:
        conn.sendall("ERRO".encode())


def processar_comando(conn, dados):
    """Interpreta e executa comandos recebidos do cliente."""

    partes = dados.split("|")

    if not partes or partes[0] == "":
        return True

    acao = partes[0]

    try:
        if acao == "UPLOAD":
            nome_arquivo = partes[1]
            tamanho = int(partes[2])
            receber_arquivo(conn, nome_arquivo, tamanho)

        elif acao == "DOWNLOAD":
            nome_arquivo = partes[1]
            enviar_arquivo(conn, nome_arquivo)

        elif acao == "LISTAR":
            listar_arquivos(conn)

        elif acao == "REMOVER":
            nome_arquivo = partes[1]
            remover_arquivo(conn, nome_arquivo)

        elif acao == "SAIR":
            return False

    except (IndexError, ValueError):
        conn.sendall("ERRO".encode())

    except (OSError, ConnectionError) as e:
        print("Erro de conexão:", e)
        return False

    return True


def cliente_thread(conn, addr):
    """Processa comandos de um cliente conectado."""

    print(f"Cliente conectado: {addr}")

    try:
        while True:
            dados = conn.recv(BUFFER_SIZE).decode()

            if not dados:
                break

            continuar = processar_comando(conn, dados)

            if not continuar:
                break

    finally:
        conn.close()
        print(f"Cliente desconectado: {addr}")


def iniciar_servidor():
    """Inicializa o servidor TCP."""

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor ouvindo em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(
            target=cliente_thread,
            args=(conn, addr),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    iniciar_servidor()
