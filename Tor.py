import time
import os
import subprocess
import requests

def check_installation():
    """Check and install necessary dependencies on Linux."""
    try:
        check_pip3 = subprocess.check_output('dpkg -s python3-pip', shell=True)
        if 'install ok installed' not in str(check_pip3):
            raise subprocess.CalledProcessError(1, 'pip3 not installed')
    except subprocess.CalledProcessError:
        print('[+] pip3 not installed')
        subprocess.check_output('sudo apt update', shell=True)
        subprocess.check_output('sudo apt install python3-pip -y', shell=True)
        print('[!] pip3 installed successfully')

    try:
        import requests
    except ImportError:
        print('[+] python3 requests is not installed')
        os.system('pip3 install requests')
        os.system('pip3 install requests[socks]')
        print('[!] python3 requests is installed')

    try:
        check_tor = subprocess.check_output('which tor', shell=True)
        if not check_tor:
            raise subprocess.CalledProcessError(1, 'tor not installed')
    except subprocess.CalledProcessError:
        print('[+] tor is not installed!')
        subprocess.check_output('sudo apt update', shell=True)
        subprocess.check_output('sudo apt install tor -y', shell=True)
        print('[!] tor is installed successfully')

    os.system("clear")

def ma_ip():
    """Get current external IP using Tor."""
    url = 'https://api.ipify.org?format=text'
    get_ip = requests.get(url, proxies=dict(http='socks5://127.0.0.1:9050', https='socks5://127.0.0.1:9050'))
    return get_ip.text

def change():
    """Change Tor IP and log the new IP."""
    os.system("service tor reload")
    new_ip = ma_ip()
    print(f'[+] Your IP has been changed to: {new_ip}')
    with open("ip_log.txt", "a") as log_file:
        log_file.write(f'{time.ctime()} - {new_ip}\n')

def main():
    check_installation()

    print('''\033[1;32;40m \n

    
     /\        | |           _____ _____  
    /  \  _   _| |_ ___      |_   _|  __ \ 
   / /\ \| | | | __/ _ \      | | | |__) | 
  / ____ \ |_| | || (_) |     | | |  ___/
 /_/    \_\__,_|\__\___/     _| |_| | 
                            |_____|_|
  

''')
   

    os.system("service tor start")

    time.sleep(3)
    print("\033[1;32;40m \nEnsure your SOCKS proxy is set to 127.0.0.1:9050 \n")

    x = input("[+] Enter the interval for changing IP (in seconds) [default=60]: ") or "60"
    lin = input("[+] Enter the number of IP changes [default=1000]. For infinite changes, type 0: ") or "1000"

    try:
        if int(lin) == 0:
            while True:
                time.sleep(int(x))
                change()
        else:
            for _ in range(int(lin)):
                time.sleep(int(x))
                change()
    except KeyboardInterrupt:
        print('\nAuto Tor is closed')

if __name__ == "__main__":
    main()
