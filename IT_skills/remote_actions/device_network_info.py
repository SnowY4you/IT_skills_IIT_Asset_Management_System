import sys
import platform
import subprocess
import logging
import os
import tkinter as tk
from tkinter import messagebox

# Configure logging
os.makedirs('IT_skills/logs', exist_ok=True)
logging.basicConfig(
    filename='IT_skills/logs/db_functions.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def log_and_print(message):
    logging.info(message)
    print(message)

# Example hostname_listbox definition
hostname_listbox = tk.Listbox()
hostname_listbox.insert(tk.END, "example_hostname")

# Get network information for selected_hostname
def get_network_info(selected_hostname):
    try:
        if platform.system().lower() == "windows":
            ipconfig_output = subprocess.check_output("ipconfig /all", shell=True)
            arp_output = subprocess.check_output("arp -a", shell=True)
        else:
            ipconfig_output = subprocess.check_output("ifconfig", shell=True)
            arp_output = subprocess.check_output("arp -a", shell=True)

        log_and_print(ipconfig_output.decode())
        log_and_print(arp_output.decode())
        return ipconfig_output.decode(), arp_output.decode()
    except subprocess.CalledProcessError as e:
        log_and_print(f"Error getting network info: {e}")
        sys.exit(1)

# Ping and trace route to selected_hostname
def ping_and_trace_route(selected_hostname):
    try:
        ping_output = subprocess.check_output(f"ping {selected_hostname}", shell=True)
        trace_output = subprocess.check_output(f"tracert {selected_hostname}", shell=True)
        log_and_print(ping_output.decode())
        log_and_print(trace_output.decode())
        return ping_output.decode(), trace_output.decode()
    except subprocess.CalledProcessError as e:
        log_and_print(f"Error pinging or tracing route: {e}")
        sys.exit(1)

# Send a release, flush and renew command to the selected_hostname
def release_flush_renew(selected_hostname):
    try:
        release_output = subprocess.check_output("ipconfig /release", shell=True)
        flush_output = subprocess.check_output("ipconfig /flushdns", shell=True)
        renew_output = subprocess.check_output("ipconfig /renew", shell=True)
        log_and_print(release_output.decode())
        log_and_print(flush_output.decode())
        log_and_print(renew_output.decode())
        return release_output.decode(), flush_output.decode(), renew_output.decode()
    except subprocess.CalledProcessError as e:
        log_and_print(f"Error releasing, flushing or renewing: {e}")
        sys.exit(1)

def network_hostname_info(parent, selected_hostname):
    network_hostname_info_window = tk.Toplevel(parent)
    network_hostname_info_window.title("Network Information")

    # Frame and Close Button (same as before)

    info_label = tk.Label(network_hostname_info_window, text=f"Network Information for {selected_hostname}:")
    info_label.pack()

    # Create Text Widgets FIRST
    ipconfig_text = tk.Text(network_hostname_info_window, wrap=tk.WORD)
    ipconfig_text.pack()

    arp_text = tk.Text(network_hostname_info_window, wrap=tk.WORD)
    arp_text.pack()

    ping_text = tk.Text(network_hostname_info_window, wrap=tk.WORD)
    ping_text.pack()

    trace_text = tk.Text(network_hostname_info_window, wrap=tk.WORD)
    trace_text.pack()

    release_text = tk.Text(network_hostname_info_window, wrap=tk.WORD)
    release_text.pack()

    flush_text = tk.Text(network_hostname_info_window, wrap=tk.WORD)
    flush_text.pack()

    renew_text = tk.Text(network_hostname_info_window, wrap=tk.WORD)
    renew_text.pack()


    # THEN call the functions and populate the widgets
    ipconfig_output, arp_output = get_network_info(selected_hostname)
    ipconfig_text.insert(tk.END, ipconfig_output)

    arp_text.insert(tk.END, arp_output)

    ping_output, trace_output = ping_and_trace_route(selected_hostname)
    ping_text.insert(tk.END, ping_output)
    trace_text.insert(tk.END, trace_output)

    release_output, flush_output, renew_output = release_flush_renew(selected_hostname)
    release_text.insert(tk.END, release_output)
    flush_text.insert(tk.END, flush_output)
    renew_text.insert(tk.END, renew_output)

