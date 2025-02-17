import tkinter as tk
from tkinter import messagebox
import random
import string
import os
from twilio.rest import Client
from ldap3 import Connection, Server, MODIFY_REPLACE

# --- Twilio Configuration (Store securely as environment variables), assuming you have a Twilio account
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

# Generate a random password
def generate_random_password(length=12):
    """Generates a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Reset the password
def reset_password(user_dn, new_password, kerberos_context):
    try:
        server = ldap3.Server('ldap://your_ldap_server', get_info=ldap3.ALL)
        connection = ldap3.Connection(server, authentication=SASL_GSSAPI, credentials=kerberos_context)
        connection.bind()

        # Correct way to modify the password:
        unicode_password = new_password.encode('utf-16le')
        password_mod = {
            'unicodePwd': [(MODIFY_REPLACE, unicode_password)]
        }
        connection.modify(user_dn, password_mod)

        connection.unbind()
        return "Password reset successfully."
    except ldap3.core.exceptions.LDAPBindError as e:
        return f"LDAP Bind Error: {e}"
    except ldap3.core.exceptions.LDAPOperationResultError as e:
        return f"LDAP Operation Error: {e}"
    except Exception as e:
        return f"LDAP Error: {e}"

# Send an SMS
def send_sms(phone_number, message):
    """Sends an SMS using Twilio."""
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_PHONE_NUMBER:
        return "Twilio configuration not found (environment variables)."

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            to=phone_number,  # The user's phone number
            from_=TWILIO_PHONE_NUMBER,  # Your Twilio number
            body=message
        )
        return "SMS sent successfully."
    except Exception as e:
        return f"SMS Error: {e}"

# Handle the password reset
def handle_password_reset(result_text, kerberos_context):  # Add result_text and kerberos_context
    try:
        username = None
        phone_number = None
        user_dn = None # Store the user DN

        username_text = result_text.get("1.0", tk.END).strip()
        for line in username_text.splitlines():
            if line.startswith("userid:"):
                username = line.split(":")[1].strip()
            if line.startswith("phone_number:"):
                phone_number = line.split(":")[1].strip()
            if line.startswith("user_dn:"): # Get the user DN
                user_dn = line.split(":")[1].strip()

        if not username:
            raise ValueError("Username not found in result_text")
        if not phone_number:
            raise ValueError("Phone number not found in result_text")
        if not user_dn:
            raise ValueError("User DN not found in result_text")

        new_password = generate_random_password()
        ldap_result = reset_password(user_dn, new_password, kerberos_context) # Pass kerberos_context

        # ... (rest of the function - same as before)

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")