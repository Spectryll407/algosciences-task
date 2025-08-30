import threading
import time
import socket
from server.tcp_server import SearchServer

def test_server_runs(tmp_path):
    test_file = tmp_path / "data.txt"
    test_file.write_text("abc\nxyz\n")

    config_file = tmp_path / "config.ini"
    config_file.write_text(f"[DEFAULT]\nlinuxpath={test_file}\nPORT=55555\nREREAD_ON_QUERY=False\n")

    server = SearchServer(config_file)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    time.sleep(0.5)  # wait for server to start

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 55555))
        s.sendall(b"abc")
        resp = s.recv(1024).decode()
        assert "EXISTS" in resp
