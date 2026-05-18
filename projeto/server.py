import socket
import threading
import os

HOST = 'localhost'
PORT = 5050
BUFFER_SIZE = 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_FILES = os.path.join(BASE_DIR, "server_files")

os.makedirs(SERVER_FILES, exist_ok=True)


def receber_arquivo(conn, nome_arquivo, tamanho):
    caminho = os.path.join(SERVER_FILES, nome_arquivo)

    with open(caminho, 'wb') as f:
        bytes_recebidos = 0

        while bytes_recebidos < tamanho:
            dados = conn.recv(min(BUFFER_SIZE, tamanho - bytes_recebidos))

            if not dados:
                break

            f.write(dados)
            bytes_recebidos += len(dados)

    print(f"Arquivo recebido: {nome_arquivo}")


def enviar_arquivo(conn, nome_arquivo):
    caminho = os.path.join(SERVER_FILES, nome_arquivo)

    if not os.path.exists(caminho):
        conn.sendall("ERRO".encode())
        return

    tamanho = os.path.getsize(caminho)

    conn.sendall(f"OK|{tamanho}".encode())

    resposta = conn.recv(BUFFER_SIZE).decode()

    if resposta != "READY":
        return

    with open(caminho, 'rb') as f:
        while chunk := f.read(BUFFER_SIZE):
            conn.sendall(chunk)

    print(f"Arquivo enviado: {nome_arquivo}")


def listar_arquivos(conn):
    arquivos = os.listdir(SERVER_FILES)

    if not arquivos:
        conn.sendall("VAZIO".encode())
        return

    lista = "\n".join(arquivos)

    conn.sendall(lista.encode())


def remover_arquivo(conn, nome_arquivo):
    caminho = os.path.join(SERVER_FILES, nome_arquivo)

    if os.path.exists(caminho):
        os.remove(caminho)
        conn.sendall("OK".encode())
        print(f"Arquivo removido: {nome_arquivo}")
    else:
        conn.sendall("ERRO".encode())


def cliente_thread(conn, addr):
    print(f"Cliente conectado: {addr}")

    while True:
        try:
            dados = conn.recv(BUFFER_SIZE).decode()

            if not dados:
                break

            comando = dados.split('|')

            acao = comando[0]

            if acao == "UPLOAD":
                nome_arquivo = comando[1]
                tamanho = int(comando[2])

                receber_arquivo(conn, nome_arquivo, tamanho)

            elif acao == "DOWNLOAD":
                nome_arquivo = comando[1]

                enviar_arquivo(conn, nome_arquivo)

            elif acao == "LISTAR":
                listar_arquivos(conn)

            elif acao == "REMOVER":
                nome_arquivo = comando[1]

                remover_arquivo(conn, nome_arquivo)

            elif acao == "SAIR":
                break

        except Exception as e:
            print("Erro:", e)
            break

    conn.close()
    print(f"Cliente desconectado: {addr}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen()

print(f"Servidor ouvindo em {HOST}:{PORT}")

while True:
    conn, addr = server.accept()

    thread = threading.Thread(target=cliente_thread, args=(conn, addr))

    thread.start()