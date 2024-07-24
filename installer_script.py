import os
import subprocess
import logging
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
    if not os.path.isfile('Tor.py'):
        print(f'[!] Tor.py does not exist in the current directory.')
        logging.error('Tor.py does not exist in the current directory.')
        sys.exit(1)

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
    if not os.path.isfile('/usr/share/aop/Tor.py') or not os.path.isfile('/usr/bin/aop'):
        print('[!] Auto Tor IP Changer is not installed.')
        logging.error('Auto Tor IP Changer is not installed.')
        sys.exit(1)

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

def main():
    """Main function to handle user input."""
    choice = input('[+] Ready to roll? Type \033[1;32mY\033[0m to install or \033[1;31mN\033[0m to uninstall >> ').strip().lower()
    
    if choice == 'y':
        install_script()
    elif choice == 'n':
        uninstall_script()
    else:
        print('[!] Invalid choice. Please type \033[1;32mY\033[0m to install or \033[1;31mN\033[0m to uninstall.')

if __name__ == "__main__":
    main()
