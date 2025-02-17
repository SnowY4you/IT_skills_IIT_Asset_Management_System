import random
import json
from faker import Faker

fake = Faker('en_US')

users = []
used_names = {}


def input_data():
    # Generate the first batch of 1000 users
    for i in range(1000):
        # Generate unique first name and last name
        first_name = fake.first_name()
        last_name = fake.last_name()

        # Generate user information
        userid = f"{first_name[:2].lower()}{last_name[:2].lower()}{random.randint(100000, 999999)}"
        phone_number = f"0{random.randint(100, 999)}-{random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}"
        email = f"{first_name.lower()}.{last_name.lower()}@iamnotreal.com"

        users.append({
            "first_name": first_name,
            "last_name": last_name,
            "userid": userid,
            "phone_number": phone_number,
            "email": email,
            "hostname": "",
            "group_id": ""
        })

    # Ensure only 10 unique first-last name combinations, used at most 3 times each
    while len(used_names) < 10:
        first_name = fake.first_name()
        last_name = fake.last_name()

        # Check if the name has been used less than 3 times
        full_name = f"{first_name} {last_name}"
        if used_names.get(full_name, 0) < 3:
            # Update usage count for the name
            used_names[full_name] = used_names.get(full_name, 0) + 1



# Run the function to populate the users list
input_data()

# Save the users data to a JSON file
with open('../data/users.json', 'w', encoding='utf-8') as f:
    json.dump(users, f, indent=4)
    print("Users data saved to users.json")