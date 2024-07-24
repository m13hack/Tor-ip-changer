import os
import subprocess
import requests
import logging
import time
import sys

# Configure logging
LOG_FILE = 'aop_installer.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_permissions(file_path):
    """Ensure the script has necessary permissions."""
    if not os.access(file_path, os.X_OK):
        logging.error(f"{file_path} does not have execute permissions.")
        print(f"[!] {file_path} does not have execute permissions.")
        sys.exit(1)

def install_script():
    """Install the Tor IP Changer script."""
    try:
        logging.info("Starting installation of Tor IP Changer script.")
        print("[+] Installing Tor IP Changer script...")

        ensure_permissions('Tor.py')

        os.makedirs('/usr/share/aop', exist_ok=True)
        subprocess.run(['cp', 'Tor.py', '/usr/share/aop/Tor.py'], check=True)

        with open('/usr/bin/aop', 'w') as file:
            file.write('#!/bin/sh\nexec python3 /usr/share/aop/Tor.py "$@"\n')
        os.chmod('/usr/bin/aop', 0o755)

        logging.info("Tor IP Changer script installed successfully.")
        print('''\n\nCongratulations! Auto Tor IP Changer is installed successfully.
From now, just type \033[1;32maop\033[0m in the terminal to run it.''')
    except subprocess.CalledProcessError as e:
        logging.error(f'Installation failed: {e}')
        print(f'[!] Installation failed: {e}')
    except Exception as e:
        logging.error(f'Unexpected error: {e}')
        print(f'[!] Unexpected error: {e}')

def uninstall_script():
    """Uninstall the Tor IP Changer script."""
    try:
        logging.info("Starting uninstallation of Tor IP Changer script.")
        print("[+] Uninstalling Tor IP Changer script...")
        subprocess.run(['rm', '-rf', '/usr/share/aop', '/usr/bin/aop'], check=True)
        logging.info("Tor IP Changer script uninstalled successfully.")
        print('[!] Auto Tor IP Changer has been removed successfully.')
    except subprocess.CalledProcessError as e:
        logging.error(f'Uninstallation failed: {e}')
        print(f'[!] Uninstallation failed: {e}')
    except Exception as e:
        logging.error(f'Unexpected error: {e}')
        print(f'[!] Unexpected error: {e}')

def check_installation():
    """Check and install necessary dependencies on Linux."""
    try:
        check_pip3 = subprocess.check_output('dpkg -s python3-pip', shell=True)
        if 'install ok installed' not in str(check_pip3):
            raise subprocess.CalledProcessError(1, 'pip3 not installed')
    except subprocess.CalledProcessError:
        logging.info('pip3 not installed')
        subprocess.check_output('sudo apt update', shell=True)
        subprocess.check_output('sudo apt install python3-pip -y', shell=True)
        logging.info('pip3 installed successfully')

    try:
        import requests
    except ImportError:
        logging.info('python3 requests is not installed')
        os.system('pip3 install requests')
        os.system('pip3 install requests[socks]')
        logging.info('python3 requests is installed')

    try:
        check_tor = subprocess.check_output('which tor', shell=True)
        if not check_tor:
            raise subprocess.CalledProcessError(1, 'tor not installed')
    except subprocess.CalledProcessError:
        logging.info('tor is not installed!')
        subprocess.check_output('sudo apt update', shell=True)
        subprocess.check_output('sudo apt install tor -y', shell=True)
        logging.info('tor is installed successfully')

    os.system("clear")

def ma_ip():
    """Get current external IP using Tor."""
    url = 'https://api.ipify.org?format=text'
    try:
        get_ip = requests.get(url, proxies=dict(http='socks5://127.0.0.1:9050', https='socks5://127.0.0.1:9050'))
        return get_ip.text
    except requests.RequestException as e:
        logging.error(f'Failed to get IP: {e}')
        print(f'[!] Failed to get IP: {e}')
        return None

def change(previous_ip):
    """Change Tor IP and log the new IP."""
    try:
        os.system("service tor reload")
        new_ip = ma_ip()
        if new_ip:
            if previous_ip:
                print(f'\n[+] IP changed from {previous_ip} to {new_ip}')
            else:
                print(f'\n[+] Your IP has been changed to: {new_ip}')
            with open("ip_log.txt", "a") as log_file:
                log_file.write(f'{time.ctime()} - {new_ip}\n')
            logging.info(f'IP changed to: {new_ip}')
    except Exception as e:
        logging.error(f'Failed to change IP: {e}')
        print(f'[!] Failed to change IP: {e}')

def main():
    """Main function to handle user input."""
    print('''\033[1;32;40m \n
     /\        | |           _____ _____  
    /  \  _   _| |_ ___      |_   _|  __ \ 
   / /\ \| | | | __/ _ \      | | | |__) | 
  / ____ \ |_| | || (_) |     | | |  ___/
 /_/    \_\__,_|\__\___/     _| |_| | 
        ver 1.0             |_____|_|
  
For help, reach out to README.md
''')
    
    check_installation()

    os.system("service tor start")
    time.sleep(3)
    print("\033[1;32;40m \nEnsure your SOCKS proxy is set to 127.0.0.1:9050 \n")

    x = input("[+] Enter the interval for changing IP (in seconds) [default=60]: ") or "60"
    lin = input("[+] Enter the number of IP changes [default=1000]. For infinite changes, type 0: ") or "1000"

    previous_ip = None

    try:
        if int(lin) == 0:
            while True:
                time.sleep(int(x))
                change(previous_ip)
                previous_ip = ma_ip()
        else:
            for _ in range(int(lin)):
                time.sleep(int(x))
                change(previous_ip)
                previous_ip = ma_ip()
    except KeyboardInterrupt:
        print('\nAuto Tor is closed')
        logging.info('Script terminated by user')

if __name__ == "__main__":
    main()
