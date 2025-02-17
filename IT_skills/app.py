import tkinter as tk
from tkinter import ttk, messagebox, Menu, Label, Button
import sqlite3
import logging
# from ldap3 import Server, Connection, SIMPLE, SYNC
import subprocess
import platform
import socket
import os
# import kerberos

from IT_skills.assign_all_ip_mac import assign_laptop_ip_mac
# from remote_actions.password_reset import handle_password_reset
from remote_actions.unlock_account import unlock_userid
# from remote_actions.clean_c_drive import main_clean_c_drive
# from remote_actions.device_network_info import network_hostname_info

# Configure logging
os.makedirs('IT_skills/IT_skills/logs', exist_ok=True)
logging.basicConfig(
    filename='IT_skills/IT_skills/logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def log_and_print(message):
    logging.info(message)
    print(message)

db_name = "itam.db"

# Kerberos Configuration (Set these appropriately for your environment)
# KRB_KDC = "your_kdc_server"  # Your Kerberos Key Distribution Center
# KRB_REALM = "YOUR.REALM"      # Your Kerberos realm
# KRB_SERVICE = "your_service_principal" # The service principal for remote actions e.g. host/computername@YOUR.REALM

# Kerberos_context = None

# def initialize_kerberos():
#    global kerberos_context
#    try:
#        # Authenticate with Kerberos (Get initial ticket)
#        kerberos_context = kerberos.authGSSClientInit(KRB_SERVICE, principal=None, gssflags=0)
#        kerberos.authGSSClientStep(kerberos_context, "")
#        log_and_print("Kerberos authentication successful.")
#        return True
#    except kerberos.GSSError as e:
#        log_and_print(f"Kerberos authentication failed: {e}")
#        return False
#    except Exception as e:
#        log_and_print(f"Error initializing Kerberos: {e}")
#        return False


# def cleanup_kerberos():
#    global kerberos_context
#    if kerberos_context:
#        kerberos.authGSSClientClean(kerberos_context)
#        kerberos_context = None
#        log_and_print("Kerberos context cleaned up.")

def on_search():
    search_text = search_entry.get().lower()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    query = """
            SELECT DISTINCT
                u.userid, u.first_name, u.last_name, u.phone_number, u.email, u.department,
                l.hostname AS laptop_hostname, l.serial_number, l.type, l.product, l.operating_system, l.processor, l.graphic_card, l.memory, l.storage, l.ip AS laptop_ip, l.mac AS laptop_mac, l.assigned_user,
                g.group_id, g.type AS group_type, g.name AS group_name,
                im.ip, im.mac,
                s.hostname AS server_hostname, s.type AS server_type, s.product AS server_product, s.ip AS server_ip,
                ug.member, ug.group_id AS ug_group_id, ug.member_type
            FROM users u
            LEFT JOIN laptops l ON u.userid = l.assigned_user
            LEFT JOIN user_groups ug ON u.userid = ug.member OR l.hostname = ug.member
            LEFT JOIN groups g ON ug.group_id = g.group_id
            LEFT JOIN hosts s ON l.hostname = s.hostname
            LEFT JOIN ip_mac im ON l.ip = im.ip OR l.mac = im.mac
            WHERE
                u.userid LIKE ? OR
                u.first_name LIKE ? OR
                u.last_name LIKE ? OR
                u.phone_number LIKE ? OR
                u.email LIKE ? OR
                u.department LIKE ? OR
                l.hostname LIKE ? OR
                l.serial_number LIKE ? OR
                l.type LIKE ? OR
                l.product LIKE ? OR
                l.operating_system LIKE ? OR
                l.processor LIKE ? OR
                l.graphic_card LIKE ? OR
                l.memory LIKE ? OR
                l.storage LIKE ? OR
                l.ip LIKE ? OR
                l.mac LIKE ? OR
                g.group_id LIKE ? OR
                g.name LIKE ? OR
                im.ip LIKE ? OR
                im.mac LIKE ? OR
                ug.member LIKE ? OR
                ug.group_id LIKE ? OR
                ug.member_type LIKE ? OR
                s.hostname LIKE ? OR
                s.type LIKE ? OR
                s.product LIKE ? OR
                s.ip LIKE ?;
            """

    search_pattern = f"%{search_text}%"
    log_and_print(f"Searching for '{search_text}'...")

    cursor.execute(query, (search_pattern,) * 28)
    results = cursor.fetchall()

    conn.close()

    output_text.delete("1.0", tk.END)
    group_info_text.delete("1.0", tk.END)

    if results:
        column_names = [description[0] for description in cursor.description]

        printed_users = set()
        printed_laptops = set()
        printed_groups = set()

        for row in results:
            row_data = dict(zip(column_names, row))

            user_id = row_data.get("userid")
            first_name = row_data.get("first_name")
            last_name = row_data.get("last_name")
            phone_number = row_data.get("phone_number")
            email = row_data.get("email")
            department = row_data.get("department")

            laptop_hostname = row_data.get("laptop_hostname")
            server_hostname = row_data.get("server_hostname")
            serial_number = row_data.get("serial_number")
            laptop_type = row_data.get("type")
            server_type = row_data.get("server_type")
            laptop_product = row_data.get("product")
            server_product = row_data.get("server_product")
            operating_system = row_data.get("operating_system")
            processor = row_data.get("processor")
            graphic_card = row_data.get("graphic_card")
            memory = row_data.get("memory")
            storage = row_data.get("storage")
            laptop_ip = row_data.get("laptop_ip")
            server_ip = row_data.get("server_ip")
            laptop_mac = row_data.get("laptop_mac")
            assigned_user = row_data.get("assigned_user")

            group_id = row_data.get("group_id")
            group_type = row_data.get("group_type")
            group_name = row_data.get("group_name")

            ip = row_data.get("ip")
            mac = row_data.get("mac")

            ug_member = row_data.get("member")
            ug_group_id = row_data.get("ug_group_id")
            ug_member_type = row_data.get("ug_member_type")

            # Define tags for text styling
            output_text.tag_configure("bold", font=("TkDefaultFont", 12, "bold"))
            output_text.tag_configure("color", foreground="darkslateblue")
            group_info_text.tag_configure("bold", font=("TkDefaultFont", 12, "bold"))
            group_info_text.tag_configure("color", foreground="darkslateblue")

            if user_id and user_id not in printed_users:
                output_text.insert(tk.END, "User Information\n", ("bold", "color"))
                output_text.insert(tk.END, "Userid: ", "bold")
                output_text.insert(tk.END, f"{user_id}\n", "user_id")
                output_text.insert(tk.END, "First name: ", "bold")
                output_text.insert(tk.END, f"{first_name}\n")
                output_text.insert(tk.END, "Last name: ", "bold")
                output_text.insert(tk.END, f"{last_name}\n")
                output_text.insert(tk.END, "Phone number: ", "bold")
                output_text.insert(tk.END, f"{phone_number}\n")
                output_text.insert(tk.END, "E-mail: ", "bold")
                output_text.insert(tk.END, f"{email}\n")
                output_text.insert(tk.END, "Department: ", "bold")
                output_text.insert(tk.END, f"{department}\n\n")

                output_text.insert(tk.END, "------------------------------------\n\n")
                printed_users.add(user_id)

            if laptop_hostname and laptop_hostname not in printed_laptops:
                output_text.insert(tk.END, "Device Information\n", ("bold", "color"))

                output_text.insert(tk.END, "Hostname: ", "bold")
                output_text.insert(tk.END, f"{laptop_hostname or server_hostname}\n", "hostname")
                output_text.insert(tk.END, "Serial number: ", "bold")
                output_text.insert(tk.END, f"{serial_number}\n")
                output_text.insert(tk.END, "Type: ", "bold")
                output_text.insert(tk.END, f"{laptop_type or server_type}\n")
                output_text.insert(tk.END, "Product: ", "bold")
                output_text.insert(tk.END, f"{laptop_product or server_product}\n")
                output_text.insert(tk.END, "Operating system: ", "bold")
                output_text.insert(tk.END, f"{operating_system}\n")
                output_text.insert(tk.END, "Processor: ", "bold")
                output_text.insert(tk.END, f"{processor}\n")
                output_text.insert(tk.END, "Graphic card: ", "bold")
                output_text.insert(tk.END, f"{graphic_card}\n")
                output_text.insert(tk.END, "Memory: ", "bold")
                output_text.insert(tk.END, f"{memory}\n")
                output_text.insert(tk.END, "Storage: ", "bold")
                output_text.insert(tk.END, f"{storage}\n")
                output_text.insert(tk.END, "IP address: ", "bold")
                output_text.insert(tk.END, f"{laptop_ip or server_ip}\n")
                output_text.insert(tk.END, "MAC address: ", "bold")
                output_text.insert(tk.END, f"{laptop_mac or mac}\n")
                output_text.insert(tk.END, "Assigned user: ", "bold")
                output_text.insert(tk.END, f"{assigned_user or user_id}\n\n")

                output_text.insert(tk.END, "------------------------------------\n\n")
                printed_laptops.add(laptop_hostname)

            # Show group information for selected user and device
            if ug_member and ug_member not in printed_users:
                group_info_text.insert(tk.END, f'Group Information for: {ug_member}\n', ("bold", "color"))
                group_info_text.insert(tk.END, "Group Name: ", "bold")
                group_info_text.insert(tk.END, f"{group_name}\n")
                group_info_text.insert(tk.END, "Group ID: ", "bold")
                group_info_text.insert(tk.END, f"{group_id}\n")
                group_info_text.insert(tk.END, "Group Type: ", "bold")
                group_info_text.insert(tk.END, f"{group_type}\n\n")

                printed_groups.add(ug_member)

            if ug_member and ug_member in printed_users:
                group_info_text.insert(tk.END, f'Group Information for: {ug_member}\n', ("bold", "color"))
                group_info_text.insert(tk.END, "Group Name: ", "bold")
                group_info_text.insert(tk.END, f"{group_name}\n")
                group_info_text.insert(tk.END, "Group ID: ", "bold")
                group_info_text.insert(tk.END, f"{group_id}\n")
                group_info_text.insert(tk.END, "Group Type: ", "bold")
                group_info_text.insert(tk.END, f"{group_type}\n\n")

                printed_groups.add(ug_member)

        def on_result_double_click(event):
            widget = event.widget
            index = widget.index("@0,%d" % event.y)
            line = widget.get(index, index + " lineend")

            try:
                if widget == output_text:
                    clicked_value = extract_value_from_output(line)
                elif widget == group_info_text:
                    clicked_value = extract_value_from_group(line)
                else:
                    return

                if clicked_value:
                    search_entry.delete(0, tk.END)
                    search_entry.insert(0, clicked_value)
                    on_search()

            except (ValueError, AttributeError) as e:
                print(f"Error extracting value: {e}")


        def extract_value_from_output(line):
            labels = ["Userid:", "First name:", "Last name:", "Phone number:", "E-mail:", "Department:", "Hostname:", "Serial number:", "Type:", "Product:", "Operating system:", "Processor:", "Graphic card:", "Memory:", "Storage:", "IP address:", "MAC address:", "Assigned user:", "Server Hostname:"]  # Add all possible labels
            for label in labels:
                if label in line:
                    return extract_value(line, label)
            return None

        def extract_value_from_group(line):
            labels = ["Group Name:", "Group ID:", "Group Type:"]
            for label in labels:
                if label in line:
                    return extract_value(line, label)
            return None


        def extract_value(line, label):
            try:
                start = line.find(label) + len(label)
                end = line.find("\n", start)
                return line[start:end].strip()
            except ValueError:
                return None


        # Bind the events AFTER populating the text widgets
        output_text.bind("<Double-Button-1>", on_result_double_click)
        group_info_text.bind("<Double-Button-1>", on_result_double_click)

    else:
        output_text.insert(tk.END, "No results found.\n")
        log_and_print("No results found.")


## Remote actions
# Define the function to assign a group to a userid in output text
def on_assign_group():
    group_frame = tk.Frame(user_tab)
    group_frame.pack(fill="both", expand=True)

    group_scrollbar = tk.Scrollbar(group_frame)
    group_scrollbar.pack(side="right", fill="y")

    group_listbox = tk.Listbox(group_frame, yscrollcommand=group_scrollbar.set)
    group_listbox.pack(side="left", fill="both", expand=True)

    group_scrollbar.config(command=group_listbox.yview)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT group_id FROM groups")
    groups = cursor.fetchall()
    conn.close()

    for group in groups:
        group_listbox.insert(tk.END, group[0])


    def assign_selected_group():
        selected_group = group_listbox.get(tk.ACTIVE)
        selected_userid = search_entry.get()

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_groups (member, group_id, member_type, type) VALUES (?, ?, (SELECT member_type FROM groups WHERE group_id = ?), ?)",
            (selected_userid, selected_group, selected_group, selected_userid))
        conn.commit()
        conn.close()

        messagebox.showinfo("Assign Group",
                            f"Group '{selected_group}' has been assigned to userid '{selected_userid}' successfully.")
        group_frame.destroy()

    assign_button = tk.Button(group_frame, text="Assign", command=assign_selected_group)
    assign_button.pack(pady=10)
    log_and_print("Opening Assign Group window.")
    log_and_print("Assigning group to userid.")
    log_and_print("Group assigned successfully.")
    log_and_print("Closing Assign Group window.")


# Define the function to assign a group to a device
def on_assign_group_device():
    group_frame = tk.Frame(asset_tab)
    group_frame.pack(fill="both", expand=True)

    group_scrollbar = tk.Scrollbar(group_frame)
    group_scrollbar.pack(side="right", fill="y")

    group_listbox = tk.Listbox(group_frame, yscrollcommand=group_scrollbar.set)
    group_listbox.pack(side="left", fill="both", expand=True)

    group_scrollbar.config(command=group_listbox.yview)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT group_id FROM groups")
    groups = cursor.fetchall()
    conn.close()

    for group in groups:
        group_listbox.insert(tk.END, group[0])

    def assign_selected_group():
        selected_group = group_listbox.get(tk.ACTIVE)
        selected_device = search_entry.get()

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_groups (member, group_id, member_type, type) VALUES (?, ?, (SELECT member_type FROM groups WHERE group_id = ?), ?)", (selected_device, selected_group, selected_group))
        conn.commit()
        conn.close()

        messagebox.showinfo("Assign Group", f"Group '{selected_group}' has been assigned to device '{selected_device}' successfully.")
        group_frame.destroy()

    assign_button = tk.Button(group_frame, text="Assign", command=assign_selected_group)
    assign_button.pack(pady=10)
    log_and_print("Opening Assign Group to Device window.")
    log_and_print("Assigning group to device.")
    log_and_print("Group assigned successfully.")
    log_and_print("Closing Assign Group to Device window.")

# Define the function to clean up C drive
def clean_c_drive():
    log_and_print("Opening Clean C Drive window")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT hostname FROM hosts")
    hosts = cursor.fetchall()
    conn.close()

    hostnames = [host[0] for host in hosts]

    def on_clean_c_drive():
        selected_hostname = hostname_listbox.get(tk.ACTIVE)

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT ip FROM ip_mac WHERE hostname = ?", (selected_hostname,))
        ip = cursor.fetchone()[0]
        conn.close()

        messagebox.showinfo("Cleaning C Drive", f"Cleaning C Drive on hostname '{selected_hostname}' with IP '{ip}'...")

        # Call the main_clean_c_drive function from the remote_actions.clean_c_drive module
        main_clean_c_drive()

        messagebox.showinfo("Cleaning C Drive", "C Drive cleanup completed.")

    clean_c_drive_window = tk.Toplevel(root)
    clean_c_drive_window.title("Clean Up C Drive")
    clean_c_drive_window.geometry("400x200")

    hostname_frame = tk.Frame(clean_c_drive_window)
    hostname_frame.pack(fill="both", expand=True)

    hostname_scrollbar = tk.Scrollbar(hostname_frame)
    hostname_scrollbar.pack(side="right", fill="y")

    hostname_listbox = tk.Listbox(hostname_frame, yscrollcommand=hostname_scrollbar.set)
    hostname_listbox.pack(side="left", fill="both", expand=True)

    hostname_scrollbar.config(command=hostname_listbox.yview)

    for hostname in hostnames:
        hostname_listbox.insert(tk.END, hostname)

    clean_button = tk.Button(clean_c_drive_window, text="Clean C Drive", command=on_clean_c_drive)
    clean_button.pack(pady=10)

# Define the function to reset password
def password_reset_handler():
    global kerberos_context
    if kerberos_context:
        handle_password_reset(output_text, kerberos_context)
    else:
        messagebox.showerror("Error", "Kerberos context is not initialized. Cannot reset password.")


# Assign IP and MAC address to hostname from laptops table in output text
def assign_ip_mac_laptop():
    log_and_print("Opening Assign IP and MAC to Laptop window")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT hostname FROM laptops")
    laptops = cursor.fetchall()
    conn.close()

    laptop_hostnames = [laptop[0] for laptop in laptops]

    def on_assign_ip_mac():
        selected_hostname = hostname_listbox.get(tk.ACTIVE)

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT ip, mac FROM ip_mac WHERE hostname = ?", (selected_hostname,))
        ip, mac = cursor.fetchone()
        conn.close()

        messagebox.showinfo("Assign IP and MAC", f"Assigning IP '{ip}' and MAC '{mac}' to hostname '{selected_hostname}'...")

        # Call the assign_laptop_ip_mac function from the assign_all_ip_mac module
        assign_laptop_ip_mac()

        messagebox.showinfo("Assign IP and MAC", "IP and MAC assignment completed.")

    assign_ip_mac_window = tk.Toplevel(root)
    assign_ip_mac_window.title("Assign IP and MAC to Laptop")
    assign_ip_mac_window.geometry("400x200")

    hostname_frame = tk.Frame(assign_ip_mac_window)
    hostname_frame.pack(fill="both", expand=True)

    hostname_scrollbar = tk.Scrollbar(hostname_frame)
    hostname_scrollbar.pack(side="right", fill="y")

    hostname_listbox = tk.Listbox(hostname_frame, yscrollcommand=hostname_scrollbar.set)
    hostname_listbox.pack(side="left", fill="both", expand=True)

    hostname_scrollbar.config(command=hostname_listbox.yview)

    for hostname in laptop_hostnames:
        hostname_listbox.insert(tk.END, hostname)

    assign_button = tk.Button(assign_ip_mac_window, text="Assign IP and MAC", command=on_assign_ip_mac)
    assign_button.pack(pady=10)

# Define the function to clean up C drive
def cleanup_laptop():
    global kerberos_context
    if kerberos_context:
        clean_c_drive(selected_hostname, kerberos_context)
    else:
        messagebox.showerror("Error", "Kerberos context is not initialized. Cannot cleanup drive.")

# Show network information for selected hostname
def show_network_info():
    global hostname_listbox
    selected_hostname = hostname_listbox.get(tk.ACTIVE)
    if selected_hostname:
        network_hostname_info(root, selected_hostname)

    else:
        messagebox.showerror("Error", "No hostname selected.")

# Assign IP address to hostname from hosts table in output text
def assign_ip_host():
    log_and_print("Opening Assign IP to Host window")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT hostname FROM hosts")
    hosts = cursor.fetchall()
    conn.close()

    hostnames = [host[0] for host in hosts]

    def on_assign_ip():
        selected_hostname = hostname_listbox.get(tk.ACTIVE)

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT ip FROM ip_mac WHERE hostname = ?", (selected_hostname,))
        ip = cursor.fetchone()[0]
        conn.close()

        messagebox.showinfo("Assign IP", f"Assigning IP '{ip}' to hostname '{selected_hostname}'...")

        # Call on_assign_ip function from the assign_ip_host module
        assign_ip_host()

        messagebox.showinfo("Assign IP", "IP assignment completed.")

    assign_ip_window = tk.Toplevel(root)
    assign_ip_window.title("Assign IP to Host")
    assign_ip_window.geometry("400x200")

    hostname_frame = tk.Frame(assign_ip_window)
    hostname_frame.pack(fill="both", expand=True)

    hostname_scrollbar = tk.Scrollbar(hostname_frame)
    hostname_scrollbar.pack(side="right", fill="y")

    hostname_listbox = tk.Listbox(hostname_frame, yscrollcommand=hostname_scrollbar.set)
    hostname_listbox.pack(side="left", fill="both", expand=True)

    hostname_scrollbar.config(command=hostname_listbox.yview)

    for hostname in hostnames:
        hostname_listbox.insert(tk.END, hostname)

    assign_button = tk.Button(assign_ip_window, text="Assign IP", command=on_assign_ip)
    assign_button.pack(pady=10)


# Root and Menu
root = tk.Tk()
root.title("Database Management")
root.config(bg="darkturquoise")
root.geometry("1400x980")
photo = tk.PhotoImage(file="C:\\Users\\svanb\\OneDrive\\Python\\Automation\\IT_skills\\savvy_trixie_icon.gif")
root.iconphoto(False, photo)


# About menu
menu = Menu(root)
root.config(menu=menu)
about_menu = Menu(menu)
menu.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "IT Assets Management System\nVersion 1.0\nDeveloped by: Your Name"))

w = Label(root, text='IT Assets Management System', bg='teal', fg='white', font=('Helvetica', 16, 'bold'))
w.grid(row=0, column=0, columnspan=3, pady=10)

search_box_frame = tk.Frame(root, bg="darkcyan", padx=1, pady=1)
search_box_frame.grid(row=1, column=0, columnspan=3, sticky="ew")

search_entry = tk.Entry(search_box_frame, width=40, font=("TkDefaultFont", 16))
search_entry.pack(side="left", padx=10, pady=10)
search_button = Button(search_box_frame, width=10, text="Search", command=on_search, font=("TkDefaultFont", 16))
search_button.pack(side="left", padx=10, pady=10)

output_frame = tk.Frame(root, bg="paleturquoise3")
output_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
output_label = tk.Label(output_frame, text="User and Device Information", bg="paleturquoise3", fg="darkcyan", font=("TkDefaultFont", 14))
output_label.pack(padx=10, pady=10)

output_text = tk.Text(output_frame, bg="paleturquoise1", wrap="word", width=40, height=40, font=("TkDefaultFont", 12))
output_text.pack(padx=20, pady=20, fill="both", expand=True)
output_text.scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
output_text.scrollbar.pack(side="right", fill="y")
output_text.config(yscrollcommand=output_text.scrollbar.set)


group_info = tk.Frame(root, bg="darkcyan", padx=1, pady=1, width=40, height=40)
group_info.grid(row=2, column=1, sticky="nsew", padx=20, pady=20)
group_label = tk.Label(group_info, text="Group Information", bg="darkcyan", fg="white", font=("TkDefaultFont", 14))
group_label.pack(padx=10, pady=10)
group_info_text = tk.Text(group_info, bg="paleturquoise1", wrap="word", width=40, height=40, font=("TkDefaultFont", 12))
group_info_text.pack(padx=20, pady=20, fill="both", expand=True)
group_info_text.scrollbar = tk.Scrollbar(group_info, command=group_info_text.yview)
group_info_text.scrollbar.pack(side="right", fill="y")
group_info_text.config(yscrollcommand=group_info_text.scrollbar.set)


# Configure the style for the notebook tabs
style = ttk.Style()
style.configure('TNotebook', background='darkcyan', foreground='white')
style.configure('TNotebook.Tab', background='cadetblue4', foreground='grey', font=('TkDefaultFont', 14))
style.map('TNotebook.Tab', background=[('selected', 'cadetblue4')], foreground=[('selected', 'black')])
style.configure('TFrame', background='paleturquoise1')

# Notebook Frame and Tabs (Corrected - create ws ONCE as LabelFrame)
ws = ttk.LabelFrame(root, text="Remote Actions", style='TFrame', padding=10)
ws.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)

notebook = ttk.Notebook(ws, style='TNotebook')
user_tab = ttk.Frame(notebook, width=300, height=40, style='TFrame')
notebook.add(user_tab, text='User')
asset_tab = ttk.Frame(notebook, width=300, height=40, style='TFrame')
notebook.add(asset_tab, text='Asset')
notebook.pack(fill="both", expand=True)


# Button Hover Effects
def on_enter(e):
    e.widget['background'] = 'cyan'
    e.widget['foreground'] = 'cadetblue4'

def on_leave(e):
    e.widget['background'] = 'darkcyan'
    e.widget['foreground'] = 'white'


password_reset_button = tk.Button(user_tab, text="Reset Password", command=password_reset_handler, bg="darkcyan", fg="white", font=("TkDefaultFont", 14))
password_reset_button.pack(pady=10)
account_unlock_button = tk.Button(user_tab, text="Account Unlock", command=unlock_userid, bg="darkcyan", fg="white", font=("TkDefaultFont", 14))
account_unlock_button.pack(pady=10)
assign_group_button = tk.Button(user_tab, text="Assign Group", command=on_assign_group, bg="darkcyan", fg="white", font=("TkDefaultFont", 14))
assign_group_button.pack(pady=10)

assign_group_to_device = tk.Button(asset_tab, text="Assign Group to Device", command=on_assign_group_device, bg="darkcyan", fg="white", font=("TkDefaultFont", 14))
assign_group_to_device.pack(pady=10)
assign_ip_mac_laptop = tk.Button(asset_tab, text="Assign IP and MAC to Laptop", command=assign_ip_mac_laptop, bg="darkcyan", fg="white", font=("TkDefaultFont", 14))
assign_ip_mac_laptop.pack(pady=10)
assign_ip_host = tk.Button(asset_tab, text="Assign IP to Host", command=assign_ip_host, bg="darkcyan", fg="white", font=("TkDefaultFont", 14))
assign_ip_host.pack(pady=10)
clean_up_c_drive = tk.Button(asset_tab, text="Clean up C drive", command=cleanup_laptop, bg="darkcyan", fg="white", font=("TkDefaultFont", 14))
clean_up_c_drive.pack(pady=10)
ping_device = tk.Button(asset_tab, text="Network Info", command=show_network_info, bg="darkcyan", fg="white", font=("TkDefaultFont", 14))
ping_device.pack(pady=10)

# Bind hover events to buttons AFTER they are created.
buttons = [password_reset_button, account_unlock_button, assign_group_button,
           assign_group_to_device, assign_ip_mac_laptop, assign_ip_host,
           clean_up_c_drive, ping_device]

for button in buttons:
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

root.mainloop()
log_and_print("Application closed.")
