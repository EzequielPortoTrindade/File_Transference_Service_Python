import socket
import os
import time

cchoice=' '
quantFolder=0
quantFile=0
cfolder=" "
aux=" "

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.settimeout(15)
client.connect(('localhost', 5050))
print('Conectado\n')
os.chdir("client/")

while cchoice!='7':
    cchoice = str(input("[1] - Criar pasta\n[2] - Envio de arquivos\n[3] - Download de arquivos\n[4] - Listar arquivos\n[5] - Remover arquivos\n[6] - Alterar pasta\n[7] - Sair\n"))
    client.send(bytes(cchoice, "utf-8"))
    os.system('clear')

    if cchoice=='1':
        #criacao da pasta
        if cfolder != " ":
            os.chdir('../')
        cfolder = str(input("Digite o nome da pasta: "))
        client.send(cfolder.encode())
        if(not os.path.exists(cfolder)):
            os.mkdir(cfolder)
        os.system('clear')
        os.chdir(cfolder)
        print("Pasta criada\n")

    elif cchoice=='2':
        #envio de arquivos
        print(cfolder)
        if cfolder!=" ":
            namefile = str(input("Digite o nome do arquivo: "))
            client.send(namefile.encode())
            size_arq = os.path.getsize(namefile)
            time.sleep(0.1)
            client.send(str(size_arq).encode())
            with open(namefile, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    client.send(data)
                    time.sleep(0.1)
            os.system('clear')
            print("Arquivo enviado\n")
        else:
            print("Pasta inexistente")

    elif cchoice=='3':
        #download de arquivos
        print(cfolder)
        if cfolder!=" ":
            namefile = str(input("Digite o nome do arquivo: ")) 
            client.sendall(namefile.encode()) 
            size_arq = int(client.recv(1024).decode())
            bytes_receive = 0
            with open(namefile, 'wb') as f:
                while bytes_receive < size_arq:
                    data = client.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    bytes_receive += len(data)
            os.system('clear')
            print("Arquivo recebido\n")
        else:
            print("Pasta inexistente")


    elif cchoice=='4':
        #listagem das pastas
        print(cfolder)
        if cfolder!=" ":
            while True:
                data = client.recv(1024).decode()
                if 'FIM' in data:
                    break
                print(data.split())
            print("\n")
        else:
            print("Pasta inexistente")
        

    elif cchoice=='5':
        #remocao de arquivos
        print(cfolder)
        if cfolder!=" ":
            namefile = str(input("Digite o nome do arquivo: "))
            if os.path.exists(namefile):
                client.send(bytes(namefile, "utf-8"))
                os.system('clear')
            else:
                print("Arquivo inexistente")
        else:
            print("Pasta inexistente")

    elif cchoice=='6':
        #alterar pasta
        if cfolder != " ":
            os.chdir('../')
        cfolder = str(input("Digite o nome da pasta: "))
        client.send(cfolder.encode())
        if os.path.exists(cfolder):
            os.chdir(cfolder)
            aux=cfolder
            os.system('clear')
            print("Pasta encontrada\n")
        else:
            cfolder=aux
            print("Pasta inexistente\n")

    elif cchoice=='7':
        print("Encerrando\n")

    else:
        print("Erro\n")

client.close()