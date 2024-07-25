import os
import subprocess

def install_script():
    """Install the Tor IP Changer script."""
    try:
        print("[+] Installing Tor IP Changer script...")
        os.chmod('Tor.py', 0o755)
        os.makedirs('/usr/share/aop', exist_ok=True)
        subprocess.run(['cp', 'Tor.py', '/usr/share/aop/Tor.py'], check=True)

        with open('/usr/bin/aop', 'w') as file:
            file.write('#!/bin/sh\nexec python3 /usr/share/aop/Tor.py "$@"')
        
        os.chmod('/usr/bin/aop', 0o755)

        print('''\n\nCongratulations! Auto Tor IP Changer is installed successfully.
From now, just type \033[1;32maop\033[0m in terminal.''')
    except subprocess.CalledProcessError as e:
        print(f'[!] Installation failed: {e}')
    except Exception as e:
        print(f'[!] Unexpected error: {e}')

def uninstall_script():
    """Uninstall the Tor IP Changer script."""
    try:
        print("[+] Uninstalling Tor IP Changer script...")
        subprocess.run(['rm', '-rf', '/usr/share/aop', '/usr/bin/aop'], check=True)
        print('[!] Auto Tor IP Changer has been removed successfully.')
    except subprocess.CalledProcessError as e:
        print(f'[!] Uninstallation failed: {e}')
    except Exception as e:
        print(f'[!] Unexpected error: {e}')

def main():
    choice = input('[+] Ready to roll? Type \033[1;32mY\033[0m to install or \033[1;31mN\033[0m to uninstall >> ').strip().lower()
    
    if choice == 'y':
        install_script()
    elif choice == 'n':
        uninstall_script()
    else:
        print('[!] Invalid choice. Please type \033[1;32mY\033[0m to install or \033[1;31mN\033[0m to uninstall.')

if __name__ == "__main__":
    main()
