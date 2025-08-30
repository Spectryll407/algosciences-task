import socket

def send_query(query: str, host="127.0.0.1", port=44445):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(query.encode("utf-8"))
        response = sock.recv(1024)
        print("Server:", response.decode("utf-8"))

if __name__ == "__main__":
    send_query("hello")
    send_query("foobar")
