import os
import sqlite3
import json
import logging

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

# Function to load data from JSON file
json_files = {
    "groups": "IT_skills\\data\\groups.json",
    "users": "IT_skills\\data\\users.json",
    "laptops": "IT_skills\\data\\laptops.json",
    "hosts": "IT_skills\\data\\hosts.json",
    "ip_mac": "IT_skills\\data\\ip_mac.json"
}

def load_data(json_file):
    """Load data from a JSON file."""
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Function to create the database and tables
def create_database(db_name):
    """Create a database and necessary tables."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON")

    # Create tables with correct schema and foreign keys
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            userid TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            phone_number TEXT,
            email TEXT,
            hostname TEXT,
            group_id TEXT,
            FOREIGN KEY (hostname) REFERENCES hosts(hostname) ON UPDATE CASCADE ON DELETE SET NULL,
            FOREIGN KEY (group_id) REFERENCES groups(group_id) ON UPDATE CASCADE ON DELETE SET NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS laptops (
            hostname TEXT PRIMARY KEY,
            serial_number TEXT,
            type TEXT,
            product TEXT,
            operating_system TEXT,
            processor TEXT,
            graphic_card TEXT,
            memory TEXT,
            storage TEXT,
            ip TEXT,
            mac TEXT,
            group_id TEXT,
            assigned_user TEXT,
            FOREIGN KEY (assigned_user) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE SET NULL,
            FOREIGN KEY (group_id) REFERENCES groups(group_id) ON UPDATE CASCADE ON DELETE SET NULL
            FOREIGN KEY (ip) REFERENCES ip_mac(ip) ON UPDATE CASCADE ON DELETE SET NULL
            FOREIGN KEY (mac) REFERENCES ip_mac(mac) ON UPDATE CASCADE ON DELETE SET NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            group_id TEXT PRIMARY KEY,
            type TEXT,
            name TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ip_mac (
            ip TEXT PRIMARY KEY,
            mac TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hosts (
            hostname TEXT PRIMARY KEY,
            type TEXT,
            product TEXT,
            ip TEXT,
            location TEXT,
            FOREIGN KEY (ip) REFERENCES ip_mac(ip) ON UPDATE CASCADE ON DELETE SET NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_groups (
            member TEXT,
            group_id TEXT,
            PRIMARY KEY (member, group_id),
            FOREIGN KEY (group_id) REFERENCES groups(group_id) ON UPDATE CASCADE ON DELETE CASCADE
            FOREIGN KEY (member) REFERENCES users(userid) ON UPDATE CASCADE ON DELETE CASCADE
            FOREIGN KEY (member) REFERENCES laptops(hostname) ON UPDATE CASCADE ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    logging.info("Database and tables created successfully.")

# Function to insert data into the specified table
def insert_data(db_name, table_name, data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    if table_name == "users":
        cursor.executemany("INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
                           [(d['userid'], d['first_name'], d['last_name'], d['phone_number'], d['email'], d['hostname'], d['group_id']) for d in data])
    elif table_name == "laptops":
        cursor.executemany("INSERT OR REPLACE INTO laptops VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           [(d['hostname'], d['serial_number'], d['type'], d['product'], d['operating_system'], d['processor'], d['graphic_card'], d['memory'], d['storage'], d['ip'], d['mac'], d['group_id'], d['assigned_user']) for d in data])
    elif table_name == "groups":
        cursor.executemany("INSERT OR REPLACE INTO groups VALUES (?, ?, ?)",
                           [(d['group_id'], d['type'], d['name']) for d in data])
    elif table_name == "ip_mac":
        cursor.executemany("INSERT OR REPLACE INTO ip_mac VALUES (?, ?)",
                           [(d['ip'], d['mac']) for d in data])
    elif table_name == "hosts":
        cursor.executemany("INSERT OR REPLACE INTO hosts VALUES (?, ?, ?, ?)",
                           [(d['hostname'], d['type'], d['product'], d['ip']) for d in data])
    elif table_name == "user_groups":
        cursor.executemany("INSERT OR REPLACE INTO user_groups VALUES (?, ?)",
                           [(d['member'], d['group_id']) for d in data])
    else:
        logging.error("Invalid table name provided.")
        print("Invalid table name provided.")
        return

    conn.commit()
    conn.close()
    logging.info(f"Data inserted into {table_name} table successfully.")

if __name__ == "__main__":
    db_name = "itam.db"
    create_database(db_name)

    for table_name, json_file in json_files.items():
        data = load_data(json_file)
        insert_data(db_name, table_name, data)
        log_and_print(f"Data inserted into {table_name} table successfully.")

    log_and_print("All data inserted successfully.")
