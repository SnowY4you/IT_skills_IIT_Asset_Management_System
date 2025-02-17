import random
import json
import string

from sklearn.compose import make_column_selector


def random_serial():
    return f"{''.join(random.choices(string.ascii_uppercase, k=2))}{''.join(random.choices(string.digits, k=8))}"

laptops = []
for i in range(1500):
    serial_number = random_serial()
    pc_name = f"PC{''.join(c for c in serial_number if c.isdigit())}"
    if i < 1200:  # 80% EliteBook 860
        laptops.append({
            "serial_number": serial_number,
            "hostname": pc_name,
            "type": "office_laptop",
            "product": "HP EliteBook 860",
            "operating_system": "Windows 11 Pro",
            "processor": "Intel® Core™ Ultra 7",
            "graphic_card": "Intel® Arc™-graphics",
            "memory": "16 GB",
            "storage": "1 TB",
            "ip": "",
            "mac": "",
            "group_id": "",
            "assigned_user": ""
        })
    else:  # 20% ZBook Studio G11
        laptops.append({
            "serial_number": serial_number,
            "hostname": pc_name,
            "type": "performance_laptop",
            "product": "HP ZBook Studio G11",
            "operating_system": "Windows 11 Pro",
            "processor": "Intel® Core™ Ultra 9",
            "graphic_card": "NVIDIA RTX™ 3000 Ada Generation",
            "memory": "64 GB",
            "storage": "1 TB",
            "ip": "",
            "mac": "",
            "group_id": "",
            "assigned_user": ""
        })

with open('../data/laptops.json', 'w', encoding='utf-8') as f:
    json.dump(laptops, f, indent=4, ensure_ascii=False)
    print("Laptops generated and saved to laptops.json")

