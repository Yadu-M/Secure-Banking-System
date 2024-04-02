import socket
import threading
import sys
import db

# users = [["u1", "p1"], ["u2", "p2"], ["u3", "p3"]]


class MultiServer(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.sock.send(b"Connected to server")
        self.username = None  # Initialize the username attribute

    def run(self):
        while True:
            data = self.sock.recv(1024).decode()
            if data.startswith("L"):
                if self.login(data[2:]):
                    break
            elif data.startswith("R"):
                if self.register(data[2:]):
                    break
            else:
                break
        if self.username:  # Proceed to message_loop only if a username is set
            self.message_loop()

    def login(self, credentials):
        username, password = credentials.split(",")
        print(username, password)
        try:
            db.auth(username, password)
        except Exception as e:
            self.sock.send(b"Login failed")
            return False
        self.sock.send(b"Login successful. You can now send messages.")
        self.username = username
        print(f"User {username} Successfully Logged In. You can now send messages.")
        return True

    def register(self, credentials):
        username, password = credentials.split(",")
        try:
            db.add_user(username, password)
        except Exception as e:
            self.sock.send(b"Username already exists")
            return False        
        users.append([username, password])
        self.sock.send(b"Registration successful. You can now send messages.")
        print(f"User {username} Successfully Registered. You can now send messages.")
        self.username = username
        return True

    def message_loop(self):
        while True:
            data = self.sock.recv(1024).decode()
            if not data or data == "EXIT":
                break
            print(f"Message from {self.username}: {data}")
            self.sock.send(f"Echo: {data}".encode())


def main(port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("localhost", port))
    server_sock.listen(5)
    print(f"Server listening on port {port}")

    while True:
        client_sock, client_address = server_sock.accept()
        MultiServer(client_sock, client_address).start()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port number>")
        sys.exit(1)

    port_number = int(sys.argv[1])
    main(port_number)
