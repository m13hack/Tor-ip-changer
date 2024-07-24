import time
import os
import subprocess
import requests

def check_installation():
    """Check and install necessary dependencies."""
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
    """Change Tor IP."""
    os.system("service tor reload")
    print('[+] Your IP has been Changed to: ' + str(ma_ip()))

def main():
    check_installation()

    print('''\033[1;32;40m \n
                _          _______
     /\        | |        |__   __|
    /  \  _   _| |_ ___      | | ___  _ __
   / /\ \| | | | __/ _ \     | |/ _ \| '__|
  / ____ \ |_| | || (_) |    | | (_) | |
 /_/    \_\__,_|\__\___/     |_|\___/|_|
                V 2.1
from mrFD
''')
    print("\033[1;40;31m http://facebook.com/ninja.hackerz.kurdish/\n")

    os.system("service tor start")

    time.sleep(3)
    print("\033[1;32;40m change your SOCKS to 127.0.0.1:9050 \n")
    os.system("service tor start")

    x = input("[+] Time to change IP in Sec [type=60] >> ")
    lin = input("[+] How many times do you want to change your IP [type=1000] for infinite IP change type [0] >> ")

    if int(lin) == 0:
        while True:
            try:
                time.sleep(int(x))
                change()
            except KeyboardInterrupt:
                print('\nAuto Tor is closed')
                quit()
    else:
        for i in range(int(lin)):
            time.sleep(int(x))
            change()

if __name__ == "__main__":
    main()
