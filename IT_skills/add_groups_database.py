import sqlite3

db_name = "itam.db"

def create_groups_table(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                group_id TEXT PRIMARY KEY,
                type TEXT,
                name TEXT,
                member_type TEXT
            )
        """)
        conn.commit()
        print("Table 'groups' created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        if conn:
            conn.close()

def add_groups_table(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        groups = [
            'ACC_GitLab_User', 'User', 'GitLab', 'User_group',
            'ACC_Workday_User', 'User', 'Workday', 'User_group',
            'ACC_ServiceNow_User', 'User', 'ServiceNow', 'User_group',
            'ACC_Jira_User', 'User', 'Jira', 'User_group',
            'ACC_Confluence_User', 'User', 'Confluence', 'User_group',
            'ACC_Azure_DevOps_User', 'User', 'Azure DevOps', 'User_group',
            'ACC_Workday_Admin', 'User', 'Workday', 'Admin_group',
            'ACC_Jira_Admin', 'User', 'Jira', 'Admin_group',
            'ACC_Confluence_Admin', 'User', 'Confluence', 'Admin_group',
            'ACC_GitLab_Admin', 'User', 'GitLab', 'Admin_group',
            'ACC_MFA_Admin', 'User', 'MFA', 'Admin_group',
            'ACC_MFA_User', 'User', 'MFA', 'User_group',
            'ACC_ServiceNow_Admin', 'User', 'ServiceNow', 'Admin_group',
            'ACC_Azure_DevOps_Admin', 'User', 'Azure DevOps', 'Admin_group',
            'ACC_Microsoft_O365_gold', 'User', 'Microsoft O365', 'MS365O_group',
            'ACC_Microsoft_O365_silver', 'User', 'Microsoft O365', 'MS365O_group',
            'ACC_Citrix_Workspace', 'User', 'Citrix Workspace', 'User_group',
            'ACC_Cloudflare_Warp', 'User', 'Cloudflare Warp', 'User_group',
            'ACC_SAP_ERP', 'User', 'SAP ERP', 'User_group',
            'ACC_VPN', 'User', 'VPN', 'User_group',
            'ACC_SAP_HANA', 'User', 'SAP HANA', 'User_group',
            'GRP_folder_path_public', 'User', 'Public Folder', 'Folder_group',
            'GRP_folder_path_A', 'User', 'Folder A', 'Folder_group',
            'GRP_folder_path_B', 'User', 'Folder B', 'Folder_group',
            'GRP_folder_path_C', 'User', 'Folder C', 'Folder_group',
            'GRP_folder_path_D', 'User', 'Folder D', 'Folder_group',
            'GRP_folder_path_E', 'User', 'Folder E', 'Folder_group',
            'GRP_folder_path_Apps', 'User', 'Apps Folder', 'Folder_group',
            'GRP_folder_path_Home_Drive', 'User', 'Home Drive', 'Folder_group',
            'NET_VPN_Access', 'User', 'VPN Access', 'VPN_group',
            'NET_VPN_Bypass', 'User', 'VPN Bypass', 'VPN_group',
            'NET_FTP_Server_01', 'User', 'FTP Server 01', 'FTP_group',
            'NET_FTP_Server_02', 'User', 'FTP Server 02', 'FTP_group',
            'IT_Team', 'User', 'IT Team', 'IT_group',
            'IT_Admin_Team', 'User', 'IT Admin Team', 'IT_group',
            'Dev_Team', 'User', 'Development Team', 'Dev_group',
            'IT_Customer_Support_Team', 'User', 'Customer Support Team', 'IT_group',
            'IT_Operations_Team', 'User', 'Operations Team', 'IT_group',
            'SG_Security_Team', 'User', 'Security Team', 'SG_group',
            'SG_Compliance_Team', 'User', 'Compliance Team', 'SG_group',
            'ACC_Workday_Admin', 'User', 'Workday', 'Admin_group',
            'ACC_Jira_Admin', 'User', 'Jira', 'Admin_group',
            'ACC_Confluence_Admin', 'User', 'Confluence', 'Admin_group',
            'DEV_GitLab_Admin', 'User', 'GitLab', 'Admin_group',
            'ACC_ServiceNow_Admin', 'User', 'ServiceNow', 'Admin_group',
            'POL_Remote_Access_Policy', 'Device', 'Remote Access Policy', 'Policy_group',
            'POL_BOYD_Policy', 'Device', 'BYOD Policy', 'Policy_group',
            'POL_Network_Security_Policy', 'Device', 'Network Security Policy', 'Policy_group',
            'POL_Asset_Management_Policy', 'Device', 'Asset Management Policy', 'Policy_group',
            'POL_Guest_Access_Policy', 'Device', 'Guest Access Policy', 'Policy_group',
            'NET_Global_Network', 'Device', 'Global Network', 'Network_group',
            'NET_Public_Network', 'Device', 'Public Network', 'Network_group',
            'NET_Firewall_lvl1', 'Device', 'Firewall Level 1', 'Network_group',
            'NET_Firewall_lvl2', 'Device', 'Firewall Level 2', 'Network_group',
            'NET_Firewall', 'Device', 'Firewall', 'Network_group',
            'POL_Access_Policy_03', 'Device', 'Access Policy 03', 'Policy_group',
            'NET_Proxy_Server_B', 'Device', 'Proxy Server B', 'Proxy_group',
            'APP_Microsoft_O365', 'Application', 'Microsoft O365', 'MS365O_group',
            'APP_Citrix_Workspace', 'Application', 'Citrix Workspace', 'User_group',
            'APP_Cloudflare_Warp', 'Application', 'Cloudflare Warp', 'User_group',
            'NET_Restricted_Network_A', 'Device', 'Restricted Network A', 'SPE_ENV_group',
            'NET_Restricted_Network_B', 'Device', 'Restricted Network B', 'SPE_ENV_group',
            'NET_Proxy_Server_Global', 'Device', 'Proxy Server Global', 'Proxy_group',
            'NET_Proxy_Server_A', 'Device', 'Proxy Server A', 'Proxy_group',
            'NET_Proxy_Server_B', 'Device', 'Proxy Server B', 'SPE_ENV_group',
            'NET_DNS_Server', 'Device', 'DNS Server', 'Network_group',
            'NET_DNS_Server_A', 'Device', 'DNS Server A', 'Network_group',
            'NET_DNS_Server_B', 'Device', 'DNS Server B', 'SPE_ENV_group',
            'NET_DHCP_Server', 'Device', 'DHCP Server', 'Network_group',
            'NET_DHCP_Server_A', 'Device', 'DHCP Server A', 'Network_group',
            'NET_DHCP_Server_B', 'Device', 'DHCP Server B', 'SPE_ENV_group',
            'APP_BeyondTrust', 'Application', 'BeyondTrust', 'User_group',
            'APP_BeyondTrust_Admin', 'Application', 'BeyondTrust', 'Admin_group',
            'APP_Company_Portal', 'Application', 'Company Portal', 'User_group',
            'APP_HP_Support_Assistant', 'Application', 'HP Support Assistant', 'User_group',
            'APP_Microsoft_Edge', 'Application', 'Microsoft Edge', 'User_group',
            'APP_7-Zip', 'Application', '7-Zip', 'User_group',
            'APP_Notepad++', 'Application', 'Notepad++', 'User_group',
            'APP_Adobe_Acrobat_Reader', 'Application', 'Adobe Acrobat Reader', 'User_group',
            'APP_VLC_Media_Player', 'Application', 'VLC Media Player', 'User_group',
            'ACC_Screensaver', 'User', 'Screensaver', 'Policy_group',
            'ACC_No_USB_Drive', 'User', 'No USB Drive', 'Policy_group'
        ]

        # Use executemany for efficiency (especially with large lists)
        data_to_insert = []
        for i in range(0, len(groups), 4):
            data_to_insert.append((groups[i], groups[i + 1], groups[i + 2], groups[i + 3]))

        cursor.executemany("""
            INSERT OR IGNORE INTO groups (group_id, type, name, member_type)
            VALUES (?, ?, ?, ?)
        """, data_to_insert)

        conn.commit()
        print(f"{len(data_to_insert)} groups added/updated successfully.")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error adding groups: {e}")
    finally:
        if conn:
            conn.close()

def show_groups_in_database(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM groups")
        groups = cursor.fetchall()

        if groups:
            print("Groups in the database:")
            for row in groups:
                print(row)
        else:
            print("No groups found in the database.")

    except sqlite3.Error as e:
        print(f"Error showing groups: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_groups_table(db_name)
    add_groups_table(db_name)
    show_groups_in_database(db_name)