<img src="IT_skills/savvy_trixie.jpg" alt="Savvy Trixie" style="float: right; margin: 4px;">

# IT Assets Management System     
## Overview
This project is an IT Assets Management System that provides a comprehensive solution for managing users, devices, and network information. The system includes a Tkinter-based GUI for easy interaction and various scripts for database management and remote actions.  
Features
- **JSON Data Generation:** Scripts to generate JSON files for computers, hosts (different types of servers), IP/MAC addresses, and users.
- **SQLite Database:*** A script to create an SQLite database with tables for users, groups, laptops, hosts, IP/MAC addresses, and user groups, including foreign key references.
- **Database Population:** Scripts to update the database with data from JSON files.
- **Group Management:** Scripts to add groups to the database and assign groups to users and laptops.
- **Device Management:** Scripts to assign laptops to users and assign IP and MAC addresses to laptops and hosts.
- **Search Functionality:** A search function with LEFT JOINs to retrieve and display user, device, and group information. Double-clicking a result refines the search.
- **Remote Actions:** A frame for remote actions, divided into user-related and device-related actions, with integration of external scripts.
- **SSO Login:** Single Sign-On (SSO) login using Kerberos for secure authentication.

## Technologies Used
- **Python:** The primary programming language for the project.
- **Tkinter:** Used for creating the graphical user interface (GUI).
- **SQLite:** A lightweight database engine used for storing and managing data.
- **Kerberos:** Used for secure SSO login.
- **LDAP3:** Used for LDAP operations such as password reset.
- **Twilio:** Used for sending SMS notifications.
- **Subprocess:** Used for executing system commands for network operations.

## Project Structure
- **JSON Data Generation:** Scripts to generate JSON files for various entities.
- **Database Creation:** A script to create an SQLite database with the necessary tables and relationships.
- **Database Population:** Scripts to populate the database with data from JSON files.
- **Group Management:** Scripts to add groups and assign them to users and laptops.
- **Device Management:** Scripts to assign IP and MAC addresses to laptops and hosts.
- **Search Functionality:** A search function to retrieve and display information with the ability to refine results by double-clicking.
- **Remote Actions:** A frame in the GUI for performing remote actions on users and devices.
- **SSO Login:** Integration of Kerberos for secure authentication.

## How to Use
- **Generate JSON Files:** Run the scripts to generate JSON files for computers, hosts, IP/MAC addresses, and users.
- **Create Database:** Run the script to create the SQLite database with the necessary tables and relationships.
- **Populate Database:** Use the scripts to update the database with data from the JSON files.
- **Manage Groups:** Add groups to the database and assign them to users and laptops using the provided scripts.
- **Manage Devices:** Assign laptops to users and assign IP and MAC addresses to laptops and hosts using the provided scripts.
- **Search Functionality:** Use the search function in the GUI to retrieve and display user, device, and group information. Double-click a result to refine the search.
- **Remote Actions:** Use the remote actions frame in the GUI to perform actions such as password reset, account unlock, and network operations.
- **SSO Login:** Use Kerberos for secure SSO login.

## Conclusion
This IT Assets Management System provides a comprehensive solution for managing users, devices, and network information. The system leverages various technologies to provide a robust and secure platform for IT asset management.