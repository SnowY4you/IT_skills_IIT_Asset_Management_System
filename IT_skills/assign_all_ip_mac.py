import sqlite3

db_name = "itam.db"

# Select column ip and mac from ip_mac table
def select_ip_and_mac(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT ip, mac FROM ip_mac")
        ip_mac = cursor.fetchall()

        return ip_mac

    except sqlite3.Error as error:
        print(f"Error: {error}")
    finally:
        if conn:
            conn.close()

# Assigning all hostnames in laptops table that have a userid in the column assigned_user with selected ip and mac addresses, ip_mac ip -> laptops ip and ip_mac mac -> laptops mac, each host their unique ip and mac
def assign_laptop_ip_mac(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        ip_mac = select_ip_and_mac(db_name)

        for ip, mac in ip_mac:
            cursor.execute("""
                UPDATE laptops
                SET ip = ?
                WHERE rowid = (
                    SELECT rowid
                    FROM laptops
                    WHERE ip = '' AND assigned_user IS NOT NULL
                    LIMIT 1
                )
            """, (ip,))

            cursor.execute("""
                UPDATE laptops
                SET mac = ?
                WHERE rowid = (
                    SELECT rowid
                    FROM laptops
                    WHERE mac = '' AND assigned_user IS NOT NULL
                    LIMIT 1
                )
            """, (mac,))

        conn.commit()
        print("IP and MAC addresses assigned successfully.")

    except sqlite3.Error as error:
        print(f"Error: {error}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    assign_laptop_ip_mac(db_name)
    print('IP and MAC addresses have been assigned successfully to laptops.')