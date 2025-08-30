import threading
import time
import socket
from pathlib import Path
from server.tcp_server import SearchServer


def test_server_runs(tmp_path):
    # Create test file
    test_file = tmp_path / "data.txt"
    test_file.write_text("abc\nxyz\n")

    # Create config.ini for this test
    config_file = tmp_path / "config.ini"
    config_file.write_text(f"""
    [DEFAULT]
    linuxpath={test_file}
    PORT=55555
    REREAD_ON_QUERY=False
    SSL=False
    HOST=127.0.0.1
    """)

    # Start server in background thread
    server = SearchServer(config_file)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    time.sleep(0.5)  # give server time to start

    # Connect with socket client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 55555))
        s.sendall(b"abc")
        resp = s.recv(1024).decode()
        assert "EXISTS" in resp

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 55555))
        s.sendall(b"nope")
        resp = s.recv(1024).decode()
        assert "NOT FOUND" in resp
