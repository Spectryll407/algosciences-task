import socket
import ssl
import threading
import logging
from server.config import Config
from server.handler import handle_request

class SearchServer:
    def __init__(self, config_path="config.ini"):
        self.config = Config(config_path)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.config.host, self.config.port))
        sock.listen(5)

        if self.config.use_ssl:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = context.wrap_socket(sock, server_side=True)

        logging.info(f"Server listening on {self.config.host}:{self.config.port}")

        while True:
            conn, addr = sock.accept()
            thread = threading.Thread(target=handle_request, args=(conn, addr, self.config))
            thread.daemon = True
            thread.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
    SearchServer().run()
