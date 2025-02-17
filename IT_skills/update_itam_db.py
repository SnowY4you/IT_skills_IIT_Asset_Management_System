import sqlite3

db_name = "itam.db"

## Trigger to update table 'users' with linked tables 'groups', 'laptops', 'ip_mac and 'user_groups'
def update_users_table(db_name):
    """Update the 'users' table with data from linked tables."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # 1. Update the 'users' table with group_id
        cursor.execute("""
            UPDATE users
            SET group_id = (
                SELECT group_id
                FROM user_groups
                WHERE user_groups.userid = users.userid
            )
        """)

        # 2. Update the 'users' table with hostname
        cursor.execute("""
            UPDATE users
            SET hostname = (
                SELECT hostname
                FROM laptops
                WHERE laptops.assigned_user = users.userid
            )
        """)

        # 3. Update the 'users' table with ip and mac
        cursor.execute("""
            UPDATE users
            SET ip = (
                SELECT ip
                FROM ip_mac
                WHERE ip_mac.hostname = users.hostname
            )
        """)
        cursor.execute("""
            UPDATE users
            SET mac = (
                SELECT mac
                FROM ip_mac
                WHERE ip_mac.hostname = users.hostname
            )
        """)

        conn.commit()
        print("Users table updated successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()


## Trigger to update table 'laptops' with linked tables 'users', 'groups', 'ip_mad and 'user_groups'
def update_laptops_table(db_name):
    """Update the 'laptops' table with data from linked tables."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # 1. Update the 'laptops' table with group_id
        cursor.execute("""
            UPDATE laptops
            SET group_id = (
                SELECT group_id
                FROM user_groups
                WHERE user_groups.hostname = laptops.hostname
            )
        """)

        # 2. Update the 'laptops' table with assigned_user
        cursor.execute("""
            UPDATE laptops
            SET assigned_user = (
                SELECT userid
                FROM users
                WHERE users.hostname = laptops.hostname
            )
        """)

        # 3. Update the 'laptops' table with ip and mac
        cursor.execute("""
            UPDATE laptops
            SET ip = (
                SELECT ip
                FROM ip_mac
                WHERE ip_mac.hostname = laptops.hostname
            )
        """)
        cursor.execute("""
            UPDATE laptops
            SET mac = (
                SELECT mac
                FROM ip_mac
                WHERE ip_mac.hostname = laptops.hostname
            )
        """)

        conn.commit()
        print("Laptops table updated successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()


## Trigger to update table 'groups' with linked tables 'users', 'laptops', and 'user_groups'
def update_groups_table(db_name):
    """Update the 'groups' table with data from linked tables."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # 1. Update the 'groups' table with user_count
        cursor.execute("""
            UPDATE groups
            SET user_count = (
                SELECT COUNT(userid)
                FROM user_groups
                WHERE user_groups.group_id = groups.group_id
            )
        """)

        # 2. Update the 'groups' table with laptop_count
        cursor.execute("""
            UPDATE groups
            SET laptop_count = (
                SELECT COUNT(hostname)
                FROM user_groups
                WHERE user_groups.group_id = groups.group_id
            )
        """)

        conn.commit()
        print("Groups table updated successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

# Trigger to update table 'user_groups' with linked tables 'users', 'laptops', and 'groups'
def update_user_groups_table(db_name):
    """Update the 'user_groups' table with data from linked tables."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # 1. Update the 'user_groups' table with group_name
        cursor.execute("""
            UPDATE user_groups
            SET group_name = (
                SELECT name
                FROM groups
                WHERE groups.group_id = user_groups.group_id
            )
        """)

        # 2. Update the 'user_groups' table with user_name
        cursor.execute("""
            UPDATE user_groups
            SET user_name = (
                SELECT name
                FROM users
                WHERE users.userid = user_groups.userid
            )
        """)

        # 3. Update the 'user_groups' table with laptop_name
        cursor.execute("""
            UPDATE user_groups
            SET laptop_name = (
                SELECT hostname
                FROM laptops
                WHERE laptops.hostname = user_groups.hostname
            )
        """)

        conn.commit()
        print("User_groups table updated successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

## Trigger to update table 'ip_mac' with linked tables 'laptops' and 'hosts'
def update_ip_mac_table(db_name):
    """Update the 'ip_mac' table with data from linked tables."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # 1. Update the 'ip_mac' table with hostname
        cursor.execute("""
            UPDATE ip_mac
            SET hostname = (
                SELECT hostname
                FROM laptops
                WHERE laptops.ip = ip_mac.ip
            )
        """)

        # 2. Update the 'ip_mac' table with host_type
        cursor.execute("""
            UPDATE ip_mac
            SET host_type = (
                SELECT type
                FROM hosts
                WHERE hosts.ip = ip_mac.ip
            )
        """)

        conn.commit()
        print("Ip_mac table updated successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

## Trigger to update table 'hosts' with linked table 'ip_mac'
def update_hosts_table(db_name):
    """Update the 'hosts' table with data from linked tables."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # 1. Update the 'hosts' table with ip
        cursor.execute("""
            UPDATE hosts
            SET ip = (
                SELECT ip
                FROM ip_mac
                WHERE ip_mac.hostname = hosts.hostname
            )
        """)

        conn.commit()
        print("Hosts table updated successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    update_users_table(db_name)
    print("Users table updated successfully.")
    update_laptops_table(db_name)
    print("Laptops table updated successfully.")
    update_groups_table(db_name)
    print("Groups table updated successfully.")
    update_user_groups_table(db_name)
    print("User_groups table updated successfully.")
    update_ip_mac_table(db_name)
    print("Ip_mac table updated successfully.")
    update_hosts_table(db_name)
    print("Hosts table updated successfully.")
    print("*** itam.db updated successfully.***")