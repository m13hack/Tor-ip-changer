import time
import subprocess
import requests
import threading

# Define colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

def check_installation():
    """Check and install necessary dependencies on Linux."""
    try:
        subprocess.run('dpkg -s python3-pip', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print(f'{YELLOW}[+] pip3 not installed{RESET}')
        try:
            subprocess.run('sudo apt update', shell=True, check=True)
            subprocess.run('sudo apt install python3-pip -y', shell=True, check=True)
            print(f'{GREEN}[!] pip3 installed successfully{RESET}')
        except subprocess.CalledProcessError as e:
            print(f'{RED}[!] Failed to install pip3: {e}{RESET}')
            return False

    try:
        import requests
    except ImportError:
        print(f'{YELLOW}[+] python3 requests is not installed{RESET}')
        try:
            subprocess.run('pip3 install requests', shell=True, check=True)
            subprocess.run('pip3 install requests[socks]', shell=True, check=True)
            print(f'{GREEN}[!] python3 requests is installed{RESET}')
        except subprocess.CalledProcessError as e:
            print(f'{RED}[!] Failed to install requests: {e}{RESET}')
            return False

    try:
        subprocess.run('which tor', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print(f'{YELLOW}[+] tor is not installed!{RESET}')
        try:
            subprocess.run('sudo apt update', shell=True, check=True)
            subprocess.run('sudo apt install tor -y', shell=True, check=True)
            print(f'{GREEN}[!] tor is installed successfully{RESET}')
        except subprocess.CalledProcessError as e:
            print(f'{RED}[!] Failed to install tor: {e}{RESET}')
            return False

    return True

def ma_ip():
    """Get current external IP using Tor."""
    url = 'https://api.ipify.org?format=text'
    try:
        response = requests.get(url, proxies={'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'})
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f'{RED}[!] Failed to get IP: {e}{RESET}')
        return None

def change_ip():
    """Change Tor IP and log the new IP."""
    try:
        subprocess.run("service tor reload", shell=True, check=True)
        new_ip = ma_ip()
        if new_ip:
            print(f'{GREEN}[+] Your IP has been changed to: {new_ip}{RESET}')
            with open("ip_log.txt", "a") as log_file:
                log_file.write(f'{time.ctime()} - {new_ip}\n')
        else:
            print(f'{RED}[!] Failed to change IP{RESET}')
    except subprocess.CalledProcessError as e:
        print(f'{RED}[!] Failed to reload Tor service: {e}{RESET}')

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
        print(f'{CYAN}\nAuto Tor is closed{RESET}')
    except Exception as e:
        print(f'{RED}[!] Unexpected error: {e}{RESET}')

def start_tor_service():
    """Start the Tor service."""
    try:
        subprocess.run("service tor start", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f'{RED}[!] Failed to start Tor service: {e}{RESET}')
        return False
    return True

def main():
    if not check_installation():
        print(f'{RED}[!] Installation checks failed. Please resolve the issues and try again.{RESET}')
        return

    print(f'''\033[1;32;40m
    
{MAGENTA} 
  /$$$$$$              /$$                     /$$$$$$ /$$$$$$$ 
 /$$__  $$            | $$                    |_  $$_/| $$__  $$
| $$  \ $$ /$$   /$$ /$$$$$$    /$$$$$$         | $$  | $$  \ $$
| $$$$$$$$| $$  | $$|_  $$_/   /$$__  $$ /$$$$$$| $$  | $$$$$$$/
| $$__  $$| $$  | $$  | $$    | $$  \ $$|______/| $$  | $$____/ 
| $$  | $$| $$  | $$  | $$ /$$| $$  | $$        | $$  | $$      
| $$  | $$|  $$$$$$/  |  $$$$/|  $$$$$$/       /$$$$$$| $$      
|__/  |__/ \______/    \___/   \______/       |______/|__/      
{RESET}
for help reach out my github: https://github.com/m13hack/Tor-ip-changer
''')

    if not start_tor_service():
        return

    time.sleep(3)
    print(f"{CYAN}\nEnsure your SOCKS proxy is set to 127.0.0.1:9050\n{RESET}")

    x = input(f"{GREEN}[+] Enter the interval for changing IP (in seconds) [default=60]: {RESET}") or "60"
    lin = input(f"{GREEN}[+] Enter the number of IP changes [default=1000]. For infinite changes, type 0: {RESET}") or "1000"

    try:
        interval = int(x)
        count = int(lin)
    except ValueError:
        print(f'{RED}[!] Invalid input. Please enter numeric values.{RESET}')
        return

    # Start the IP change process in a separate thread to improve performance
    change_thread = threading.Thread(target=change_ips_continuously, args=(interval, count))
    change_thread.start()

if __name__ == "__main__":
    main()
