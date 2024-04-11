import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import actions
import json
import socket


# ------------------------------------------------------Defining Socket Stuff----------------------------------------#
HOST_NAME = "localhost"
PORT_NUM = 15000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST_NAME, PORT_NUM))
print(sock.recv(1024).decode())

user = ""
balanceGlobal = ""

# ------------------------------------------------------UI Stuff------------------------------------------------------#

root = tk.Tk()
root.title("ATM Machine")

# Create a frame for the title
title_frame = ttk.Frame(root)
title_frame.pack(pady=10)

# Title
title_label = ttk.Label(title_frame, text="ATM Machine", font=("Arial", 18, "bold"))
title_label.pack()

# Create a frame for the login/register page
login_frame = ttk.Frame(root)
login_frame.pack(pady=20)

# Username
username_label = ttk.Label(login_frame, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry = ttk.Entry(login_frame)
username_entry.grid(row=0, column=1, padx=10, pady=10)

# Password
password_label = ttk.Label(login_frame, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)


# Post login/register page
def post_login():
    login_frame.forget()        

    # Create a frame for the transaction page
    transaction_frame = ttk.Frame(root)
    transaction_frame.pack(pady=20)

    data_to_send = {
        "action": actions.BALANCE
    }

    encoded_data = json.dumps(data_to_send).encode()
    sock.send(encoded_data)

    ogbalance = sock.recv(1024).decode()

    # Current Balance
    current_balance_label = ttk.Label(transaction_frame, text=f"Current Balance: {ogbalance}")
    current_balance_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Withdraw
    withdraw_label = ttk.Label(transaction_frame, text="Withdraw:")
    withdraw_label.grid(row=1, column=0, padx=10, pady=10)
    withdraw_entry = ttk.Entry(transaction_frame)
    withdraw_entry.grid(row=1, column=1, padx=10, pady=10)

    # Deposit
    deposit_label = ttk.Label(transaction_frame, text="Deposit:")
    deposit_label.grid(row=2, column=0, padx=10, pady=10)
    deposit_entry = ttk.Entry(transaction_frame)
    deposit_entry.grid(row=2, column=1, padx=10, pady=10)

    # Validate input
    def validate_input(action, input_str, input_field):
        if action != '1':
            return True
        try:
            value = int(input_str)
            if value < 0:
                return False
            if input_field == 'withdraw' and deposit_entry.get():
                return False
            if input_field == 'deposit' and withdraw_entry.get():
                return False
        except ValueError:
            return False
        return True

    # Restrict input to numbers
    withdraw_entry.config(validate='key', validatecommand=(withdraw_entry.register(lambda action, input_str: validate_input(action, input_str, 'withdraw')), '%d', '%P'))
    deposit_entry.config(validate='key', validatecommand=(deposit_entry.register(lambda action, input_str: validate_input(action, input_str, 'deposit')), '%d', '%P'))

    # Confirm button
    def confirm():

        global user

        withdraw_amount = withdraw_entry.get()
        deposit_amount = deposit_entry.get()
        # Add your transaction logic here
        if deposit_amount:
            print("User", user, int(deposit_amount))
            # deposit(user, int(deposit_amount))
            data_to_send = {
                "action": actions.DEPOSIT,
                "amount": deposit_amount,
            }

            encoded_data = json.dumps(data_to_send).encode()
            sock.send(encoded_data)
            response = sock.recv(1024).decode()
            print("new balance: ", response)
            current_balance_label.configure(text=f"Current Balance: {response}")
        elif withdraw_amount:
            # dsd
            print("User", user, int(withdraw_amount))
            # deposit(user, int(deposit_amount))
            data_to_send = {
                "action": actions.WITHDRAW,
                "amount": withdraw_amount,
            }

            encoded_data = json.dumps(data_to_send).encode()
            sock.send(encoded_data)
            response = sock.recv(1024).decode()
            print("new balance: ", response)
            current_balance_label.configure(text=f"Current Balance: {response}")
        else:
            print("NON ACTION REQUESTED")

    confirm_button = ttk.Button(transaction_frame, text="Confirm", command=confirm)
    confirm_button.grid(row=3, column=0, columnspan=2, pady=10)


# Login button
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    # print(username, password)
    
    global user
    
    # Sending User Data to 
    data_to_send = {
        "action": actions.LOGIN,
        "username": username,
        "password": password
    }
    
    encoded_data = json.dumps(data_to_send).encode()
    sock.send(encoded_data)
    response = sock.recv(1024).decode()
    # response_obj = json.loads(response)
    
    print(response)
    # print(response_obj)
    # print(f'Register Status: {response}\n')    

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
    elif response == "Error":
        messagebox.showerror("Invalid Credentials", "Wrong credentials entered")
    else:
        user = username
        post_login()


login_button = ttk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=0, padx=10, pady=10)

# Register button
def register():
    username = username_entry.get()
    password = password_entry.get()

    global user

    # Sending user data to server
    data = {
        "action": actions.REGISTER,
        "username": username,
        "password": password
    }

    encoded_data = json.dumps(data).encode()
    sock.send(encoded_data)
    response = sock.recv(1024).decode()

    if (response == "Username already exists"):
        messagebox.showerror("Error", "Username already exists.")
    else:
        response_obj = json.loads(response)

        print(response_obj)    
        print(f'Register Status: {response}\n')    

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
        elif not response:
            messagebox.showerror("Error", "Something went wrong while trying to register")
        else:
            deposit = response_obj["balance"]
            user = username
            post_login()

register_button = ttk.Button(login_frame, text="Register", command=register)
register_button.grid(row=2, column=1, padx=10, pady=10)


root.mainloop()
