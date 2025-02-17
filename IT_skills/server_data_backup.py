import paramiko
import os
import smtplib
from email.mime.text import MIMEText

# Server details
servers = [
    {"host": "server1.example.com", "username": "user", "password": "password"},
    {"host": "server2.example.com", "username": "user", "password": "password"},
]

backup_dir = "/path/to/backup"
log_file = "/path/to/log_file.log"


def connect_to_server(server):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server["host"], username=server["username"], password=server["password"])
    return ssh


def check_server_status(ssh):
    stdin, stdout, stderr = ssh.exec_command("uptime")
    return stdout.read().decode()


def backup_data(ssh, server):
    sftp = ssh.open_sftp()
    sftp.get("/path/to/important/data", os.path.join(backup_dir, f"{server['host']}_data_backup"))
    sftp.close()


def send_report(log):
    msg = MIMEText(log)
    msg['Subject'] = 'Backup and Synchronization Report'
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'admin@example.com'

    with smtplib.SMTP('smtp.example.com') as server:
        server.login('your_email@example.com', 'your_password')
        server.sendmail('your_email@example.com', ['admin@example.com'], msg.as_string())


def main():
    log = ""
    for server in servers:
        ssh = connect_to_server(server)
        status = check_server_status(ssh)
        log += f"{server['host']} status: {status}\n"
        backup_data(ssh, server)
        log += f"Backup completed for {server['host']}\n"
        ssh.close()

    with open(log_file, 'w') as file:
        file.write(log)

    send_report(log)


if __name__ == "__main__":
    main()
