import sqlite3

db_name = "itam.db"

base_groups_users = [
    'ACC_GitLab_User',
    'ACC_SAP_HANA',
    'ACC_Cloudflare_Warp',
    'ACC_SAP_ERP',
    'ACC_Workday_User',
    'ACC_ServiceNow_User',
    'ACC_Jira_User',
    'ACC_Confluence_User',
    'ACC_Microsoft_O365_silver',
    'GRP_folder_path_public',
    'ACC_VPN',
    'NET_FTP_Server_01',
    'NET_FTP_Server_02',
    'ACC_MFA_User'
]

laptop_groups = [
    'APP_BeyondTrust',
    'APP_Company_Portal',
    'APP_HP_Support_Assistant',
    'APP_Microsoft_Edge',
    'APP_7-Zip',
    'APP_Notepad++',
    'APP_Adobe_Acrobat_Reader',
    'APP_VLC_Media_Player',
    'ACC_Screensaver',
    'ACC_No_USB_Drive',
    'APP_Microsoft_O365',
    'APP_Citrix_Workspace',
    'APP_Cloudflare_Warp',
    'APP_IBM_Maximo',
    'ACC_Citrix_Workspace',
    'ACC_Firewall',
    'ACC_Proxy_Server',
    'NET_Firewall_lvl1',
    'NET_Global_Network',
    'NET_DNS_Server',
    'POL_Microsoft_O365_silver',
    'POL_Password_Policy',
    'POL_Remote_Access_Policy',
    'POL_BOYD_Policy',
    'POL_Network_Security_Policy',
    'POL_Asset_Management_Policy',
    'POL_Guest_Access_Policy'
]


def assign_department_groups(cursor):
    cursor.execute("SELECT userid, department FROM users")
    users = cursor.fetchall()

    for userid, department in users:
        if department == 'IT':
            cursor.execute("INSERT OR IGNORE INTO user_groups (member, group_id, member_type) VALUES (?, 'IT_Customer_Support_Team', (SELECT member_type FROM groups WHERE group_id = 'IT_Customer_Support_Team'))", (userid,))
            cursor.execute("""
                INSERT OR IGNORE INTO user_groups (member, group_id, member_type)
                SELECT ?, group_id, member_type FROM groups WHERE member_type = 'Admin_group'
                ORDER BY RANDOM() LIMIT (SELECT COUNT(userid) * 0.8 FROM users WHERE department = 'IT')
            """, (userid,))
            cursor.execute("INSERT OR IGNORE INTO user_groups (member, group_id, member_type) VALUES (?, 'IT_Admin_Team', (SELECT member_type FROM groups WHERE group_id = 'IT_Admin_Team'))", (userid,))
            cursor.execute("""
                INSERT OR IGNORE INTO user_groups (member, group_id, member_type)
                SELECT ?, group_id, member_type FROM groups WHERE member_type = 'Admin_group'
                ORDER BY RANDOM() LIMIT (SELECT COUNT(userid) * 0.6 FROM users WHERE department = 'IT')
            """, (userid,))
            cursor.execute("INSERT OR IGNORE INTO user_groups (member, group_id, member_type) VALUES (?, 'IT_Operations_Team', (SELECT member_type FROM groups WHERE group_id = 'IT_Operations_Team'))", (userid,))
            cursor.execute("""
                INSERT OR IGNORE INTO user_groups (member, group_id, member_type)
                SELECT ?, group_id, member_type FROM groups WHERE member_type = 'SG_group'
                ORDER BY RANDOM() LIMIT (SELECT COUNT(userid) * 0.05 FROM users WHERE department = 'IT')
            """, (userid,))
            cursor.execute("INSERT OR IGNORE INTO user_groups (member, group_id, member_type) VALUES (?, 'Dev_Team', (SELECT member_type FROM groups WHERE group_id = 'Dev_Team'))", (userid,))
        elif department == 'R&D':
            cursor.execute("INSERT OR IGNORE INTO user_groups (member, group_id, member_type) VALUES (?, 'Dev_Team', (SELECT member_type FROM groups WHERE group_id = 'Dev_Team'))", (userid,))
            cursor.execute("""
                INSERT OR IGNORE INTO user_groups (member, group_id, member_type)
                SELECT ?, group_id, member_type FROM groups WHERE member_type = 'Admin_group'
            """, (userid,))
        elif department == 'Special Environment':
            cursor.execute("""
                INSERT OR IGNORE INTO user_groups (member, group_id, member_type)
                SELECT ?, group_id, member_type FROM groups WHERE member_type = 'SPE_ENV_group'
            """, (userid,))
        elif department == 'Administration':
            cursor.execute("INSERT OR IGNORE INTO user_groups (member, group_id, member_type) VALUES (?, 'ACC_Jira_Admin', (SELECT member_type FROM groups WHERE group_id = 'ACC_Jira_Admin'))", (userid,))
            cursor.execute("INSERT OR IGNORE INTO user_groups (member, group_id, member_type) VALUES (?, 'ACC_Workday_Admin', (SELECT member_type FROM groups WHERE group_id = 'ACC_Workday_Admin'))", (userid,))
            cursor.execute("INSERT OR IGNORE INTO user_groups (member, group_id, member_type) VALUES (?, 'ACC_Confluence_Admin', (SELECT member_type FROM groups WHERE group_id = 'ACC_Confluence_Admin'))", (userid,))
        elif department == 'HR':
            cursor.execute("INSERT OR IGNORE INTO user_groups (member, group_id, member_type) VALUES (?, 'ACC_Jira_Admin', (SELECT member_type FROM groups WHERE group_id = 'ACC_Jira_Admin'))", (userid,))
            cursor.execute("INSERT OR IGNORE INTO user_groups (member, group_id, member_type) VALUES (?, 'ACC_Workday_Admin', (SELECT member_type FROM groups WHERE group_id = 'ACC_Workday_Admin'))", (userid,))
            cursor.execute("INSERT OR IGNORE INTO user_groups (member, group_id, member_type) VALUES (?, 'ACC_Confluence_Admin', (SELECT member_type FROM groups WHERE group_id = 'ACC_Confluence_Admin'))", (userid,))
        print(f"Assigned department groups for user {userid} in department {department}")


# Assign each laptop all the groups defined in: laptop_groups
def assign_laptop_groups(cursor):
    cursor.execute("SELECT hostname FROM laptops WHERE assigned_user IS NOT NULL")
    assigned_laptops = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT group_id FROM groups WHERE group_id IN ({})".format(','.join(['?']*len(laptop_groups))), laptop_groups)
    laptop_groups_ids = [row[0] for row in cursor.fetchall()]

    for laptop in assigned_laptops:
        for group in laptop_groups_ids:
            cursor.execute("INSERT OR IGNORE INTO user_groups (member, group_id, member_type) VALUES (?, ?, (SELECT member_type FROM groups WHERE group_id = ?))", (laptop, group, group))
        print(f"Assigned laptop groups for laptop {laptop}")


# Assign each user all the groups defined in: base_groups_users
def assign_base_groups(cursor):
    cursor.execute("SELECT userid FROM users")
    users = cursor.fetchall()

    for user in users:
        for group in base_groups_users:
            cursor.execute("INSERT OR IGNORE INTO user_groups (member, group_id, member_type) VALUES (?, ?, (SELECT member_type FROM groups WHERE group_id = ?))", (user[0], group, group))
        print(f"Assigned base groups for user {user[0]}")

if __name__ == "__main__":
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        assign_department_groups(cursor)
        print("Department groups: IT, R&D, Special Environment, Administration, HR assigned to users successfully.")
        assign_laptop_groups(cursor)
        print("Laptop groups assigned to users successfully.")

        assign_base_groups(cursor)
        print("Base groups assigned to users successfully.")

        conn.commit()
        print("Groups assigned successfully.")

        # Check how many userds i table users have not been assigned to any group
        # Check how my laptops have not been assigned to any group
        # Check how many groups have no members
        # Check how many userids have been assigned to multiple groups or any group at all
        cursor.execute("SELECT COUNT(userid) FROM users WHERE userid NOT IN (SELECT member FROM user_groups)")
        users_no_group = cursor.fetchone()[0]
        print(f"Users not assigned to any group: {users_no_group}")

        cursor.execute("SELECT COUNT(hostname) FROM laptops WHERE hostname NOT IN (SELECT member FROM user_groups)")
        laptops_no_group = cursor.fetchone()[0]
        print(f"Laptops not assigned to any group: {laptops_no_group}")

        cursor.execute("SELECT COUNT(group_id) FROM groups WHERE group_id NOT IN (SELECT group_id FROM user_groups)")
        groups_no_members = cursor.fetchone()[0]
        print(f"Groups without members: {groups_no_members}")

        cursor.execute("SELECT COUNT(DISTINCT member) FROM user_groups")
        users_assigned_unique = cursor.fetchone()[0]
        print(f"Users assigned to unique groups: {users_assigned_unique}")

        # Average number of groups per user
        cursor.execute("SELECT AVG(groups_per_user) FROM (SELECT COUNT(group_id) AS groups_per_user FROM user_groups GROUP BY member)")
        avg_groups_per_user = cursor.fetchone()[0]
        print(f"Average number of groups per user: {avg_groups_per_user}")

        # Average number of users per group
        cursor.execute("SELECT AVG(users_per_group) FROM (SELECT COUNT(member) AS users_per_group FROM user_groups GROUP BY group_id)")
        avg_users_per_group = cursor.fetchone()[0]
        print(f"Average number of users per group: {avg_users_per_group}")

        # Average number of groups per laptop
        cursor.execute("SELECT AVG(groups_per_laptop) FROM (SELECT COUNT(group_id) AS groups_per_laptop FROM user_groups WHERE member IN (SELECT hostname FROM laptops) GROUP BY member)")
        avg_groups_per_laptop = cursor.fetchone()[0]
        print(f"Average number of groups per laptop: {avg_groups_per_laptop}")







    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

