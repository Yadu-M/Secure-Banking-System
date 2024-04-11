import socket
import threading
import sys
import db
import json
import actions

PORT_NUM = 15000


class MultiServer(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.sock.send(b"Connected to server")
        self.username = None  # Initialize the username attribute
        self.auth = False
        self.balance = None

    def run(self):
        while True:
            data : dict
            incoming_data = self.sock.recv(1024).decode()    
            data = json.loads(incoming_data)

            print(data)      
            action = data["action"]

            if action == actions.LOGIN:
                self.login(data)
            elif action == actions.REGISTER:
                self.register(data)

            if self.username:  # Proceed to message_loop only if a username is set
                self.message_loop()

    def login(self, user_data):
        username = user_data["username"]
        password = user_data["password"]
        balance = None
        try:
            balance = db.auth(username, password)
        except:
            self.sock.send(b"Error")
            return False

        obj_to_send = {"status": True, "balance": f"{balance}"}

        self.sock.send(json.dumps(obj_to_send).encode("utf-8"))
        self.username = username
        self.auth = True
        self.balance = balance
        # print(f"User {username} Successfully Logged In. You can now send messages.")
        return True

    def register(self, user_data):
        username = user_data["username"]
        password = user_data["password"]
        balance = 0
        try:
            db.add_user(username, password)
        except Exception as e:
            self.sock.send(b"Username already exists")
            return False   
        obj_to_send = {"status": True, "balance": f"{balance}"}

        self.sock.send(json.dumps(obj_to_send).encode("utf-8"))
        print(f"User {username} Successfully Registered. You can now send messages.")
        self.auth = True
        self.username = username
        self.balance = balance
        return True

    def message_loop(self):
        print("In Messaghe LOOP")
        while True:
            incoming_data = self.sock.recv(1024).decode()
            data = json.loads(incoming_data)
            action = data["action"]

            if not data or data == "EXIT":
                break

            print(f"Message from {self.username}: {data}")

            if action == actions.DEPOSIT:
                data["amount"] = int(data["amount"])
                print("data b4 action", data)

                newBalance = db.deposit(self.username, data["amount"])
                print(newBalance)
                self.sock.send(str(newBalance).encode())
                # print("test1")
            elif action == actions.WITHDRAW:
                data["amount"] = int(data["amount"])
                action = data["action"]
                print("data b4 action", data)

                newBalance = db.withdraw(self.username, data["amount"])
                print(newBalance)
                self.sock.send(str(newBalance).encode())
            elif action == actions.BALANCE:
                checkbalance = db.getBalance(self.username)
                print(checkbalance)
                self.sock.send(str(checkbalance).encode())
            else:
                print("The action you are attempting does not exist.")

            # self.sock.send(f"Echo: {data}".encode())


def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("localhost", PORT_NUM))
    server_sock.listen(5)
    print(f"Server listening on port {PORT_NUM}")

    while True:
        client_sock, client_address = server_sock.accept()
        MultiServer(client_sock, client_address).start()


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python server.py <port number>")
    #     sys.exit(1)

    # port_number = int(sys.argv[1])
    main()
