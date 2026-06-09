import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import server

def test_listar_arquivos_vazio(tmp_path, monkeypatch):
    monkeypatch.setattr(server, "SERVER_FILES", tmp_path)

    class FakeConn:
        def __init__(self):
            self.data = None

        def sendall(self, msg):
            self.data = msg.decode()

    conn = FakeConn()

    server.listar_arquivos(conn)

    assert conn.data == "VAZIO"

def test_listar_arquivos_com_arquivos(tmp_path, monkeypatch):
    monkeypatch.setattr(server, "SERVER_FILES", tmp_path)

    (tmp_path / "a.txt").write_text("A")
    (tmp_path / "b.txt").write_text("B")

    class FakeConn:
        def __init__(self):
            self.data = None

        def sendall(self, msg):
            self.data = msg.decode()

    conn = FakeConn()

    server.listar_arquivos(conn)

    assert "a.txt" in conn.data
    assert "b.txt" in conn.data

def test_remover_arquivo(tmp_path, monkeypatch):
    monkeypatch.setattr(server, "SERVER_FILES", tmp_path)

    file = tmp_path / "teste.txt"
    file.write_text("conteudo")

    class FakeConn:
        def __init__(self):
            self.msg = None

        def sendall(self, msg):
            self.msg = msg.decode()

    conn = FakeConn()

    server.remover_arquivo(conn, "teste.txt")

    assert not file.exists()
    assert conn.msg == "OK"

def test_remover_arquivo_inexistente(tmp_path, monkeypatch):
    monkeypatch.setattr(server, "SERVER_FILES", tmp_path)

    class FakeConn:
        def __init__(self):
            self.msg = None

        def sendall(self, msg):
            self.msg = msg.decode()

    conn = FakeConn()

    server.remover_arquivo(conn, "nao_existe.txt")

    assert conn.msg == "ERRO"

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
    assert file.exists()