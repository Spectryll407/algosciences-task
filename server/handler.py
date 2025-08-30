import time
import logging
from server.search import linear_search, cached_set_search

def handle_request(conn, addr, config):
    logging.info(f"Connection from {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            query = data.decode("utf-8").strip().replace("\x00", "")
            start = time.perf_counter()

            if config.reread_on_query:
                found = linear_search(query, config.file_path)
            else:
                found = cached_set_search(query, config.file_path)

            elapsed = (time.perf_counter() - start) * 1000
            response = "STRING EXISTS\n" if found else "STRING NOT FOUND\n"

            logging.debug(f"DEBUG: {query} from {addr}, {elapsed:.2f}ms")
            conn.sendall(response.encode("utf-8"))
