import socket
import threading
import sys
import db
import json
import actions
from threading import Lock
from tabulate import tabulate


# Initialize a Lock and a shared list
auditLogLock = Lock()
auditLogTracker = []
auditLogHeaders = ["Customer ID", "Customer Username", "Action Taken", "Date/Time Of Action"]
from cryptography.fernet import Fernet 
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib
import base64
import hmac
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
        self.key = None
        self.keyValue = None
        self.key1 = None
        self.key2 = None

    def addLog(self, username: str, action: str):
        global shared_list, shared_list_lock
        with auditLogLock:
            identity, time = db.getIDAndTime(username)
            row = [identity, username, action, time]
            auditLogTracker.append(row)
            table = tabulate(
                auditLogTracker,
                auditLogHeaders,
                tablefmt="plain",
                colalign=("left", "left", "left", "left")
            )

            with open("auditlog.txt", "w") as f:
                f.write(table)


    def run(self):
        counter = 0
        while True:
            print (counter)
            data : dict
            if counter >= 1:
                incoming_data = self.key.decrypt(self.sock.recv(1024))
                incoming_data = incoming_data.decode()
            if counter == 0:    
                incoming_data = self.sock.recv(1024).decode()  
            data = json.loads(incoming_data)
            print(data)      
            action = data["action"]

            if action == actions.LOGIN:
                self.login(data)
            elif action == actions.REGISTER:
                self.register(data)
            elif action == actions.KEY:
                print (data["KEY"])
                key = data["KEY"].encode()
                self.key = Fernet(key)
                self.keyValue = key
                counter +=1 
            


            if self.username:  # Proceed to message_loop only if a username is set
                self.message_loop()


    def keyDerive(self):
        salt = os.urandom(16)
        # derive
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=80000,
        )
        key1 = kdf.derive(self.keyValue)
        #print ("key1")
        #print (key1)
        sha256_hash1 = hashlib.sha256(key1).digest()
        base64_encoded1 = base64.b64encode(sha256_hash1)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=80001,
        )
        key2 = kdf.derive(self.keyValue)
        #print ("key2")
        #print (key2)
        sha256_hash2 = hashlib.sha256(key2).digest()
        base64_encoded2 = base64.b64encode(sha256_hash2)

        # verify
        #print (base64_encoded1)
        #print (base64_encoded2)
        #keystr = key.decode()
        #print (keystr)
    

        return (base64_encoded1, base64_encoded2)

    def login(self, user_data):
        username = user_data["username"]
        password = user_data["password"]
        balance = None
        key1, key2 = self.keyDerive()
        self.key1 = Fernet(key1)
        self.key2 = key2
        print ("key1 is")
        print (key1)
        print ("key2 is")
        print (key2)
        key1 = key1.decode()
        key2 = key2.decode()
        #print (key1)
        #print (key2)
        try:
            balance = db.auth(username, password)

        except:
            self.sock.send(b"Error")
            return False

        obj_to_send = {"status": True, "balance": f"{balance}", "key1": key1, "key2": key2}
        encoded_data = json.dumps(obj_to_send).encode()
        token = self.key.encrypt(encoded_data) 
        self.sock.send(token)
        #self.sock.send(json.dumps(obj_to_send).encode("utf-8"))
        self.username = username
        self.auth = True
        self.balance = balance
        # print(f"User {username} Successfully Logged In. You can now send messages.")
        return True

    def register(self, user_data):
        username = user_data["username"]
        password = user_data["password"]
        balance = 0
        key1, key2 = self.keyDerive()
        self.key1 = Fernet(key1)
        self.key2 = key2
        print ("key1 is")
        print (key1)
        print ("key2 is")
        print (key2)
        key1 = key1.decode()
        key2 = key2.decode()
        try:
            db.add_user(username, password)
        except Exception as e:
            self.sock.send(b"Username already exists")
            return False
        print ("in register key1")
        print (key1)
        obj_to_send = {"status": True, "balance": f"{balance}", "key1": key1, "key2": key2}
        encoded_data = json.dumps(obj_to_send).encode()
        token = self.key.encrypt(encoded_data) 
        self.sock.send(token)
        print(f"User {username} Successfully Registered. You can now send messages.")
        self.auth = True
        self.username = username
        self.balance = balance
        return True

    def message_loop(self):
        print("In Messaghe LOOP")
        self.addLog(self.username, f"The user logged in.")
        while True:
            
            incoming_data = self.key1.decrypt(self.sock.recv(1024))
            incoming_data = incoming_data.decode()
            data = json.loads(incoming_data)
            action = data["action"]

            if not data or data == "EXIT":
                break

            print(f"Message from {self.username}: {data}")
            if action == actions.DEPOSIT:
                #HMAC START
                message = {
                    "action": action,
                    "amount": data["amount"]
                }
                encoded_data = json.dumps(message).encode()
                received_base64_hmac = data["sig"]

                calculated_hmac_digest = hmac.new(self.key2, encoded_data, hashlib.sha256).digest()
                calculated_base64_hmac = base64.b64encode(calculated_hmac_digest).decode('utf-8')

                if calculated_base64_hmac == received_base64_hmac:
                    print("Signatures match. The message is authentic.")
                else:
                    print("Signatures do not match. The message may have been tampered with.")
                #HMAC END
                data["amount"] = int(data["amount"])
                amount = data["amount"]
                print("data b4 action", data)

                newBalance = db.deposit(self.username, data["amount"])
                print(newBalance)
                self.sock.send(str(newBalance).encode())
                self.addLog(
                    self.username,
                    f"The user deposited ${amount}'s. New balance is ${newBalance}.",
                )
            elif action == actions.WITHDRAW:
                #HMAC START
                message = {
                    "action": action,
                    "amount": data["amount"]
                }
                encoded_data = json.dumps(message).encode()
                received_base64_hmac = data["sig"]

                calculated_hmac_digest = hmac.new(self.key2, encoded_data, hashlib.sha256).digest()
                calculated_base64_hmac = base64.b64encode(calculated_hmac_digest).decode('utf-8')

                if calculated_base64_hmac == received_base64_hmac:
                    print("Signatures match. The message is authentic.")
                else:
                    print("Signatures do not match. The message may have been tampered with.")
                #HMAC END



                data["amount"] = int(data["amount"])
                amount = data["amount"]
                print("data b4 action", data)

                newBalance = db.withdraw(self.username, data["amount"])
                print(newBalance)
                self.sock.send(str(newBalance).encode())
                self.addLog(
                    self.username,
                    f"The user withdrew ${amount}'s. New balance is ${newBalance}.",
                )
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

    # f = open("auditlog.txt", "w")
    # f.write("Customer ID \t|\tCustomer Username\t|\tAction Taken\t|\tTime Of Action")
    # f.close()

    while True:
        client_sock, client_address = server_sock.accept()
        MultiServer(client_sock, client_address).start()


if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python server.py <port number>")
    #     sys.exit(1)

    # port_number = int(sys.argv[1])
    main()
