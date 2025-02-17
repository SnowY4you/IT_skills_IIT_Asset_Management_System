import tkinter as tk
from tkinter import messagebox
from ldap3 import Connection, Server, MODIFY_REPLACE


# Unlock the userid from 'result_text' under 'userid'
def unlock_userid():
    # Get the userid
    user_id = result_text.split("userid: ")[1].split("\n")[0]

    # Connect to the LDAP server
    server = Server(LDAP_SERVER)
    conn = Connection(server, user=LDAP_BIND_DN, password=LDAP_BIND_PASSWORD)
    conn.bind()

    # Unlock the account
    conn.modify(f"uid={user_id},{LDAP_BASE_DN}", {'pwdAccountLockedTime': [(MODIFY_REPLACE, [])]})

    # Check if the account is unlocked
    conn.search(f"uid={user_id},{LDAP_BASE_DN}", '(objectclass=*)', attributes=['pwdAccountLockedTime'])
    if 'pwdAccountLockedTime' in conn.entries[0]:
        messagebox.showerror("Error", "Failed to unlock the account.")
    else:
        messagebox.showinfo("Success", "Account unlocked successfully.")
