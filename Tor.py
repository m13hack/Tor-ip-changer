import time
import os
import subprocess
import requests
import threading

def check_installation():
    """Check and install necessary dependencies on Linux."""
    try:
        check_pip3 = subprocess.check_output('dpkg -s python3-pip', shell=True)
        if 'install ok installed' not in str(check_pip3):
            raise subprocess.CalledProcessError(1, 'pip3 not installed')
    except subprocess.CalledProcessError:
        print('[+] pip3 not installed')
        try:
            subprocess.check_output('sudo apt update', shell=True)
            subprocess.check_output('sudo apt install python3-pip -y', shell=True)
            print('[!] pip3 installed successfully')
        except subprocess.CalledProcessError as e:
            print(f'[!] Failed to install pip3: {e}')
            return False

    try:
        import requests
    except ImportError:
        print('[+] python3 requests is not installed')
        try:
            os.system('pip3 install requests')
            os.system('pip3 install requests[socks]')
            print('[!] python3 requests is installed')
        except Exception as e:
            print(f'[!] Failed to install requests: {e}')
            return False

    try:
        check_tor = subprocess.check_output('which tor', shell=True)
        if not check_tor:
            raise subprocess.CalledProcessError(1, 'tor not installed')
    except subprocess.CalledProcessError:
        print('[+] tor is not installed!')
        try:
            subprocess.check_output('sudo apt update', shell=True)
            subprocess.check_output('sudo apt install tor -y', shell=True)
            print('[!] tor is installed successfully')
        except subprocess.CalledProcessError as e:
            print(f'[!] Failed to install tor: {e}')
            return False

    os.system("clear")
    return True

def ma_ip():
    """Get current external IP using Tor."""
    url = 'https://api.ipify.org?format=text'
    try:
        get_ip = requests.get(url, proxies=dict(http='socks5://127.0.0.1:9050', https='socks5://127.0.0.1:9050'))
        return get_ip.text
    except requests.RequestException as e:
        print(f'[!] Failed to get IP: {e}')
        return None

def change_ip():
    """Change Tor IP and log the new IP."""
    try:
        os.system("service tor reload")
        new_ip = ma_ip()
        if new_ip:
            print(f'[+] Your IP has been changed to: {new_ip}')
            with open("ip_log.txt", "a") as log_file:
                log_file.write(f'{time.ctime()} - {new_ip}\n')
        else:
            print('[!] Failed to change IP')
    except Exception as e:
        print(f'[!] Failed to change IP: {e}')

def change_ips_continuously(interval, count):
    """Change IPs at specified intervals."""
    try:
        if count == 0:
            while True:
                time.sleep(interval)
                change_ip()
        else:
            for _ in range(count):
                time.sleep(interval)
                change_ip()
    except KeyboardInterrupt:
        print('\nAuto Tor is closed')
    except Exception as e:
        print(f'[!] Unexpected error: {e}')

def start_tor_service():
    """Start the Tor service."""
    try:
        os.system("service tor start")
    except Exception as e:
        print(f'[!] Failed to start Tor service: {e}')
        return False
    return True

def main():
    if not check_installation():
        print('[!] Installation checks failed. Please resolve the issues and try again.')
        return

    print('''\033[1;32;40m \n

    
     /\        | |           _____ _____  
    /  \  _   _| |_ ___      |_   _|  __ \ 
   / /\ \| | | | __/ _ \      | | | |__) | 
  / ____ \ |_| | || (_) |     | | |  ___/
 /_/    \_\__,_|\__\___/     _| |_| | 
        ver 1.0             |_____|_|
  
for help reach out my github: https://github.com/m13hack/Tor-ip-changer
''')

    if not start_tor_service():
        return

    time.sleep(3)
    print("\033[1;32;40m \nEnsure your SOCKS proxy is set to 127.0.0.1:9050 \n")

    x = input("[+] Enter the interval for changing IP (in seconds) [default=60]: ") or "60"
    lin = input("[+] Enter the number of IP changes [default=1000]. For infinite changes, type 0: ") or "1000"

    try:
        interval = int(x)
        count = int(lin)
    except ValueError:
        print('[!] Invalid input. Please enter numeric values.')
        return

    # Start the IP change process in a separate thread to improve performance
    change_thread = threading.Thread(target=change_ips_continuously, args=(interval, count))
    change_thread.start()

if __name__ == "__main__":
    main()
