import logging
import sqlite3
import os
import shutil
import subprocess
import platform
import glob
import kerberos

db_name = "itam.db"

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

# Function to delete files
def delete_files(paths):
    for path in paths:
        for item in glob.glob(path):
            try:
                if os.path.isfile(item):
                    os.remove(item)
                elif os.path.isdir(item):
                    shutil.rmtree(item)
                print(f"Deleted: {item}")
            except Exception as e:
                print(f"Error deleting {item}: {e}")

# Get free space on C drive
def get_free_space(selected_hostname):
    try:
        free_space = subprocess.check_output(f"wmic /node:{selected_hostname} logicaldisk where caption='C:' get FreeSpace", shell=True)
        free_space = free_space.decode().split('\n')[1].strip()
        return int(free_space)
    except subprocess.CalledProcessError as e:
        print(f"Error getting free space: {e}")
        return 0

def show_free_space(selected_hostname):
    free_space = get_free_space(selected_hostname)
    print(f"Free space on C drive: {free_space / (1024 * 1024 * 1024):.2f} GB")

def clean_temp_files(selected_hostname):
    print("Cleaning temporary files...")
    temp_paths = [
        os.path.join(os.getenv('TEMP'), '*'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', '*'),
        os.path.join(os.getenv('WINDIR'), 'Temp', '*')
    ]
    delete_files(temp_paths)

def clean_teams_cache(selected_hostname):
    print("Cleaning Teams cache...")
    teams_cache_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Teams', 'Cache', '*')
    delete_files([teams_cache_path])

def clean_system_files(selected_hostname):
    print("Cleaning system files...")
    system_paths = [
        os.path.join(os.getenv('WINDIR'), 'SoftwareDistribution', 'Download', '*'),
        os.path.join(os.getenv('WINDIR'), 'System32', 'LogFiles', 'WMI', 'RtBackup', '*')
    ]
    delete_files(system_paths)

def clean_software_distribution(selected_hostname):
    print("Cleaning Software Distribution folder...")
    software_distribution_path = os.path.join(os.getenv('WINDIR'), 'SoftwareDistribution', 'Download', '*')
    delete_files([software_distribution_path])

def clean_outlook_cache(selected_hostname):
    print("Cleaning Outlook cache...")
    outlook_cache_paths = [
        os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Outlook', 'OfficeFileCache', '*'),
        os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Outlook', 'RoamCache', '*')
    ]
    delete_files(outlook_cache_paths)

def clean_adobe_flash(selected_hostname):
    print("Cleaning Adobe Flash cache...")
    adobe_flash_cache_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Adobe', 'Flash Player', 'NativeCache', '*')
    delete_files([adobe_flash_cache_path])

def clean_sccm_cache(selected_hostname):
    print("Cleaning SCCM cache...")
    sccm_cache_path = os.path.join(os.getenv('WINDIR'), 'ccmcache', '*')
    delete_files([sccm_cache_path])

def main_clean_c_drive(selected_hostname, context):
    try:
        # Remote execution (using hostname and context)
        command = f"psexec \\\\{selected_hostname} cmd.exe /c 'cleanmgr /sagerun:1'"
        env = os.environ.copy()
        env['KRB5CCNAME'] = os.path.join(os.getcwd(), 'krb5cc')
        subprocess.run(command, check=True, env=env)
        print(f"Cleaned C drive on {selected_hostname}")

        free_space_before = get_free_space(selected_hostname)
        clean_temp_files(selected_hostname)
        clean_teams_cache(selected_hostname)
        clean_system_files(selected_hostname)
        clean_software_distribution(selected_hostname)
        clean_outlook_cache(selected_hostname)
        clean_adobe_flash(selected_hostname)
        clean_sccm_cache(selected_hostname)
        free_space_after = get_free_space(selected_hostname)
        freed_space = (free_space_after - free_space_before) / (1024 * 1024 * 1024)
        print(f"PC cleanup completed. Freed up space: {freed_space:.2f} GB")
        print(f"Free space available now: {free_space_after / (1024 * 1024 * 1024):.2f} GB")

        return freed_space, free_space_after

    except subprocess.CalledProcessError as e:
        print(f"Error cleaning C drive on {selected_hostname}: {e}")

        raise
    except Exception as e:
        print(f"An unexpected error occurred on {selected_hostname}: {e}")

        raise
