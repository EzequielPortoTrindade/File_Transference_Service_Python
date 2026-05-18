import socket
import os

HOST = 'localhost'
PORT = 5050
BUFFER_SIZE = 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_FILES = os.path.join(BASE_DIR, "client_files")

os.makedirs(CLIENT_FILES, exist_ok=True)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

print("Conectado ao servidor")


def upload():
    nome_arquivo = input("Nome do arquivo: ")

    caminho = os.path.join(CLIENT_FILES, nome_arquivo)

    if not os.path.exists(caminho):
        print("Arquivo não encontrado")
        return

    tamanho = os.path.getsize(caminho)

    mensagem = f"UPLOAD|{nome_arquivo}|{tamanho}"

    client.sendall(mensagem.encode())

    with open(caminho, 'rb') as f:
        while chunk := f.read(BUFFER_SIZE):
            client.sendall(chunk)

    print("Upload concluído")


def download():
    nome_arquivo = input("Nome do arquivo: ")

    mensagem = f"DOWNLOAD|{nome_arquivo}"

    client.sendall(mensagem.encode())

    resposta = client.recv(BUFFER_SIZE).decode()

    if resposta == "ERRO":
        print("Arquivo não encontrado no servidor")
        return

    _, tamanho = resposta.split('|')

    tamanho = int(tamanho)

    client.sendall("READY".encode())

    caminho = os.path.join(CLIENT_FILES, nome_arquivo)

    with open(caminho, 'wb') as f:
        bytes_recebidos = 0

        while bytes_recebidos < tamanho:
            dados = client.recv(min(BUFFER_SIZE, tamanho - bytes_recebidos))

            if not dados:
                break

            f.write(dados)
            bytes_recebidos += len(dados)

    print("Download concluído")


def listar():
    client.sendall("LISTAR".encode())

    dados = client.recv(BUFFER_SIZE).decode()

    if dados == "VAZIO":
        print("Nenhum arquivo")
        return

    print("\nArquivos no servidor:\n")
    print(dados)


def remover():
    nome_arquivo = input("Nome do arquivo: ")

    mensagem = f"REMOVER|{nome_arquivo}"

    client.sendall(mensagem.encode())

    resposta = client.recv(BUFFER_SIZE).decode()

    if resposta == "OK":
        print("Arquivo removido")
    else:
        print("Arquivo não encontrado")


while True:
    print("\n[1] Upload")
    print("[2] Download")
    print("[3] Listar")
    print("[4] Remover")
    print("[5] Sair")

    opcao = input("Escolha: ")

    if opcao == '1':
        upload()

    elif opcao == '2':
        download()

    elif opcao == '3':
        listar()

    elif opcao == '4':
        remover()

    elif opcao == '5':
        client.sendall("SAIR".encode())

        break

    else:
        print("Opção inválida")

client.close()