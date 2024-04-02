import socket
import sys


def main(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(sock.recv(1024).decode())

    while True:
        action = input("Enter 'L' to log in or 'R' to register: ").strip().upper()
        if action in ["L", "R"]:
            username = input("Username: ")
            password = input("Password: ")
            message = f"{action} {username},{password}"
            sock.send(message.encode())
            response = sock.recv(1024).decode()
            print(response)
            if "successful" in response:
                break
        else:
            print(
                "Invalid option. Please choose 'L' for login or 'R' for registration."
            )

    print("You can now start sending messages. Type 'EXIT' to quit.")
    while True:
        msg = input()
        if msg == "EXIT":
            sock.send(msg.encode())
            break
        sock.send(msg.encode())
        echo = sock.recv(1024).decode()
        print(echo)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <host name> <port number>")
        sys.exit(1)

    host_name = sys.argv[1]
    port_number = int(sys.argv[2])
    main(host_name, port_number)
