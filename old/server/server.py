import socket
import os
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5050))
os.chdir("server/")
status = 0
while True:
    if status==0:
        schoice=' '
        quantFolder=0
        quantFile=0
        sfolder = " "
        aux = " "
        server.listen(5)
        print('Esperando conexões...\n')
        connection, address = server.accept()
        status = 1
        print('Conectado\n')

    schoice = connection.recv(1024).decode()
    if schoice=='1':
        #criacao de pasta
        if sfolder != " ":
            os.chdir('../')
        sfolder = connection.recv(1024).decode()
        if(not os.path.exists(sfolder)):
            os.mkdir(sfolder)
        os.chdir(sfolder)
        print("Pasta criada\n")

    elif schoice=='2':
        #envio de arquivos
        print(sfolder)
        if sfolder!=" ":
            namefile = connection.recv(1024).decode()
            print(namefile)
            size_arq = int(connection.recv(1024).decode())
            bytes_receive = 0
            with open(namefile, 'wb') as f:
                while bytes_receive < size_arq:
                    data = connection.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    bytes_receive += len(data)
            print("Arquivo recebido\n")
        else:
            print("Pasta inexistente")

    elif schoice=='3':
        #download de arquivos
        print(sfolder)
        if sfolder!=" ":
            namefile = connection.recv(1024).decode()
            print(namefile)
            size_arq = os.path.getsize(namefile)
            connection.send(str(size_arq).encode())
            with open(namefile, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    connection.send(data)
                    time.sleep(0.1)
            print("Arquivo enviado\n")
        else:
            print("Pasta inexistente")
            
        
    elif schoice=='4':
        #listagem das pastas
        print(sfolder)
        if sfolder!=" ":
            datas = os.listdir()
            for data in datas:
                connection.sendall(f'{data}\n'.encode())
                time.sleep(0.1)
            connection.sendall(b'FIM')
        else:
            print("Pasta inexistente\n")

    elif schoice=='5':
        #remocao de arquivos
        print(sfolder)
        if sfolder!=" ":
            namefile = connection.recv(1024).decode()
            if os.path.exists(namefile):
                os.remove(namefile)
            else:
                print("Arquivo inexistente\n")
        else:
            print("Pasta inexistente")    
    
    elif schoice=='6':
        #alterar pasta
        if sfolder != " ":
            os.chdir('../')
        sfolder = connection.recv(1024).decode()
        if os.path.exists(sfolder):
            os.chdir(sfolder)
            aux=sfolder
            print("Pasta encontrada\n")
        else:
            sfolder = aux
            print("Pasta inexistente\n")

    elif schoice=='7':
        status = 0
        os.chdir('../')
        os.system("clear")
        print("Encerrando\n")
        
connection.close()
server.close()
#/home/codespace/.python/current/bin/python3 /workspaces/codespaces-blank/client/client.py