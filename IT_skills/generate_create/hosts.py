import json
import random

# List to store all generated hostnames
hostnames = []

# Generate hostnames for SQL database servers
products_sql = ["Microsoft SQL Server", "MySQL", "Oracle Database"]
for _ in range(40):
    hostname = f"SQL_{random.randint(100, 999)}"
    hostnames.append({
        "hostname": hostname,
        "type": "sql_server",
        "product": random.choice(products_sql),
        "ip": ""
    })

# Generate hostnames for AP routers
products_ap = ["Cisco", "Aruba"]
for _ in range(30):
    hostname = f"AP_{random.randint(100, 999)}"
    hostnames.append({
        "hostname": hostname,
        "type": "ap_router",
        "product": random.choice(products_ap),
        "ip": ""
    })

# Generate hostnames for switches
products_switch = ["Cisco", "Dell", "HP"]
for _ in range(20):
    hostname = f"Switch_{random.randint(100, 999)}"
    hostnames.append({
        "hostname": hostname,
        "type": "switch",
        "product": random.choice(products_switch),
        "ip": ""
    })

# Generate hostnames for firewalls
products_firewall = ["Palo Alto"]
for _ in range(20):
    hostname = f"Firewall_{random.randint(100, 999)}"
    hostnames.append({
        "hostname": hostname,
        "type": "firewall",
        "product": random.choice(products_firewall),
        "ip": ""
    })

# Generate hostnames for storage servers
products_storage = ["HPE", "Windows Server"]
for _ in range(50):
    hostname = f"Storage_{random.randint(100, 999)}"
    hostnames.append({
        "hostname": hostname,
        "type": "storage_server",
        "product": random.choice(products_storage),
        "ip": ""
    })

# Generate hostnames for DNS servers
products_dns = ["Azure DNS"]
for _ in range(20):
    hostname = f"DNS_{random.randint(100, 999)}"
    hostnames.append({
        "hostname": hostname,
        "type": "dns_server",
        "product": random.choice(products_dns),
        "ip": ""
    })

# Generate hostnames for mail servers
products_mail = ["Microsoft Exchange"]
for _ in range(20):
    hostname = f"Mail_{random.randint(100, 999)}"
    hostnames.append({
        "hostname": hostname,
        "type": "mail_server",
        "product": random.choice(products_mail),
        "ip": ""
    })

# Generate hostnames for VMs
products_vm = ["VMware", "Hyper-V"]
for _ in range(50):
    hostname = f"VM_{random.randint(100, 999)}"
    hostnames.append({
        "hostname": hostname,
        "type": "vm_server",
        "product": random.choice(products_vm),
        "ip": ""
    })

# Generate hostnames for VPN servers
products_vpn = ["Palo Alto"]
for _ in range(20):
    hostname = f"VPN_{random.randint(100, 999)}"
    hostnames.append({
        "hostname": hostname,
        "type": "vpn_server",
        "product": random.choice(products_vpn),
        "ip": ""
    })

# Generate hostnames for proxy servers
products_proxy = ["Palo Alto"]
for _ in range(10):
    hostname = f"Proxy_{random.randint(100, 999)}"
    hostnames.append({
        "hostname": hostname,
        "type": "proxy_server",
        "product": random.choice(products_proxy),
        "ip": ""
    })

# Generate hostnames for FTP servers
products_ftp = ["FileZilla"]
for _ in range(10):
    hostname = f"FTP_{random.randint(100, 999)}"
    hostnames.append({
        "hostname": hostname,
        "type": "ftp_server",
        "product": random.choice(products_ftp),
        "ip": ""
    })

# Save to JSON file
with open('../data/hosts.json', 'w') as f:
    json.dump(hostnames, f, indent=4)
    print("Hostnames generated and saved to hosts.json")
