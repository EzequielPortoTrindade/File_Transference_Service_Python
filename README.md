#  Desenvolver um serviço de transferência de arquivos com as seguintes características:

#  Criação de pasta no servidor a partir do cliente
#  Alteração de pasta no cliente e no servidor
#  Envio de arquivo
#  Download de arquivo
#  Listagem da pasta
#  Remoção de arquivo no servidor

# Comandos para utilização
    py server.py
    py client.py

# Como iniciar?

 1. abra dois terminais e execute "py server.py" em um deles (ou execute o comando com & no mesmo terminal);

 2. após isso, execute "py client.py" no segundo terminal e acesse o menu.



 # Analise estática 

 pylint server.py client.py

 mypy server.py client.py

 bandit server.py client.py

 # Teste unitário

 pytest -v 

# interessante considerar

Como observação técnica, é interessante notar que o Bandit não sinalizou o uso de os.path.join(..., nome_arquivo) porque ele nem sempre consegue inferir que o nome do arquivo vem diretamente da rede. Em uma revisão manual de segurança, ainda seria recomendável validar o nome do arquivo recebido do cliente usando algo como os.path.basename(nome_arquivo) para reduzir riscos de acesso indevido a caminhos de arquivos. Isso pode ser citado como uma melhoria futura no trabalho.


pytest -v
=============== test session starts ================
platform win32 -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0 -- C:\Users\Lenovo\Desktop\Trabalho_Rede_de_Computadores\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Lenovo\Desktop\Trabalho_Rede_de_Computadores\projeto
collected 5 items                                   

tests/test_server.py::test_listar_arquivos_vazio PASSED [ 20%]
tests/test_server.py::test_listar_arquivos_com_arquivos PASSED [ 40%]
tests/test_server.py::test_remover_arquivo PASSED [ 60%]
tests/test_server.py::test_remover_arquivo_inexistente PASSED [ 80%]
tests/test_server.py::test_path_traversal_protection FAILED [100%]

===================== FAILURES =====================
__________ test_path_traversal_protection __________

tmp_path = WindowsPath('C:/Users/Lenovo/AppData/Local/Temp/pytest-of-Lenovo/pytest-7/test_path_traversal_protection0')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x00000205C5A838A0>

    def test_path_traversal_protection(tmp_path, monkeypatch):
        monkeypatch.setattr(server, "SERVER_FILES", tmp_path)
    
        file = tmp_path / "seguro.txt"
        file.write_text("ok")
    
        class FakeConn:
            def sendall(self, msg):
                pass
    
        conn = FakeConn()
    
        # tentativa de ataque
        server.remover_arquivo(conn, "../../seguro.txt")
    
        # o arquivo NÃO deve ser removido
>       assert file.exists()
E       AssertionError: assert False
E        +  where False = exists()
E        +    where exists = WindowsPath('C:/Users/Lenovo/AppData/Local/Temp/pytest-of-Lenovo/pytest-7/test_path_traversal_protection0/seguro.txt').exists

tests\test_server.py:96: AssertionError
--------------- Captured stdout call ---------------
Arquivo removido: seguro.txt
============= short test summary info ==============
FAILED tests/test_server.py::test_path_traversal_protection - AssertionError: assert False
=========== 1 failed, 4 passed in 0.49s ============