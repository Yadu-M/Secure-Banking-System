from tkinter import *
import tkinter as tk

SCREEN_SIZE = "1080x720"
APPLICATION_TITLE = "ATM Machine"

user = ""
user_pass = ""

root = tk.Tk()
root.pack_propagate(False)

widgets_to_hide = []

# --------------------------------Main Screen Stuff------------------------------------- #
root.title("ATM Machine")
root.geometry(SCREEN_SIZE)
label = tk.Label(root, text=APPLICATION_TITLE, pady="10")
label.pack()

# ---------------------------Event handler functions and stuff--------------------------- #
def register_user(username_entry, password_entry):
    for widget in widgets_to_hide:
        widget.grid_forget()
    widgets_to_hide.clear()
    user = username_entry.get()
    user_pass = password_entry.get()
    
    success_msg = tk.Label(root, text=f'Account has been successfully registered with Username: {user}')
    success_msg.grid(row=3, column=3, padx=10, pady=10)
    # print(user, user_pass)
    #TODO Here is the main entyr point (Show deposit,withdraw.... options)
    
def on_register(username_entry, password_entry):
    for widget in widgets_to_hide:
        widget.grid_forget()
    widgets_to_hide.clear()

    username_label = tk.Label(root, text="Username: ")
    username_label.grid(row=0, column=0, padx=5, pady=50, sticky="e")
    username_entry.grid(row=0, column=1, padx=5, pady=5)
    password_label = tk.Label(root, text="Password:")
    password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    password_entry.grid(row=1, column=1, padx=5, pady=5)
    actual_register_btn = tk.Button(root, text="Register Account", command=lambda: register_user(username_entry, password_entry))
    actual_register_btn.grid(row=2, column=1, padx=5, pady=5)
    widgets_to_hide.append(username_label)
    widgets_to_hide.append(password_label)
    widgets_to_hide.append(actual_register_btn)
    widgets_to_hide.append(username_entry)
    widgets_to_hide.append(password_entry)

def show_login_widgets(username_label, username_entry, password_label, password_entry, login_button):
    print('start of show login widgets')

    for widget in widgets_to_hide:
        widget.grid_forget()
    widgets_to_hide.clear()

    username_label.grid(row=0, column=0, padx=5, pady=50, sticky="e")
    username_entry.grid(row=0, column=1, padx=5, pady=5)
    password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    password_entry.grid(row=1, column=1, padx=5, pady=5)
    login_button.grid(row=2, column=1, padx=5, pady=5)

def on_login():
    username = username_entry.get()
    password = password_entry.get()
    if username != user or password != user_pass:
        # Removing all the labels and entries and stuff
        username_label.grid_forget()
        username_entry.grid_forget()
        password_label.grid_forget()
        password_entry.grid_forget()
        login_button.grid_forget()

        prompt_label = tk.Label(root, text="User with this username or password is not found.\nIf you don't have an account, please register.")
        prompt_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        widgets_to_hide.append(prompt_label)

        register_button = tk.Button(root, text="Register", command=lambda: on_register(username_entry, password_entry)) #command=on_register(username_entry, password_entry)
        register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        widgets_to_hide.append(register_button)

        try_again_btn = tk.Button(root, text="Try again", command=lambda: show_login_widgets(username_label, username_entry, password_label, password_entry, login_button))
        try_again_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        widgets_to_hide.append(try_again_btn)
    
    else:
        pass
        #TODO Here is the main entyr point (Show deposit,withdraw.... options)

# ------------------------------User Name/Password stuff-------------------------- #
username_label = tk.Label(root, text="Username: ")
username_label.grid(row=0, column=0, padx=5, pady=50, sticky="e")
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=5, pady=5)

password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
password_entry = tk.Entry(root, show="*")  # This will hide the password characters
password_entry.grid(row=1, column=1, padx=5, pady=5)

login_button = tk.Button(root, text="Login", command=on_login)
login_button.grid(row=2, column=1, padx=5, pady=5)

# ----------------------------------------------------------------------------------------- #
root.mainloop()