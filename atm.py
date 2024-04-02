from tkinter import *
import tkinter as tk

SCREEN_SIZE = "1080x720"
APPLICATION_TITLE = "ATM Machine"

root = tk.Tk()
root.pack_propagate(False)


#--------------------------------Main Screen Stuff-------------------------------------#
root.title("ATM Machine")

root.geometry(SCREEN_SIZE)
label = tk.Label(root, text=APPLICATION_TITLE, pady="10")
label.pack()



#---------------------------Event handler functions and stuff---------------------------#

def on_register():
    print('register success!')
    
def on_login():
    username = username_entry.get()
    password = password_entry.get()
    print(username, password)


#--------------------------------Register Stuff--------------------------------------#
register_btn = tk.Button(root, text="Register", command=on_register)




#------------------------------User Name/Password stuff--------------------------#
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


#TODO If user entered the wrong password prompt them to
#Either reenter or are them if they registered (show the register button as well under)


#-----------------------------------------------------------------------------------------#

root.mainloop()