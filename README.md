# Tor-ip-changer

# Auto IP Changer

**Auto IP Changer** is a Python script designed to automate the process of changing your IP address using Tor. This tool can be useful for various purposes, including maintaining anonymity and circumventing IP-based restrictions.

## Features

- **Automated IP Changes:** Automatically changes your IP address at regular intervals.
- **Flexible Configuration:** Easily set the interval for IP changes and the number of changes.
- **Logging:** Local logging of IP changes and errors for troubleshooting.
- **Easy Installation:** Simple installation and uninstallation scripts provided.
- **Compatibility:** Designed to work on Linux systems with Tor installed.

## Installation

To install the Auto IP Changer script, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/FDX100/Auto_Tor_IP_changer.git
   cd Auto_Tor_IP_changer
   ```

2. **Run the Installer Script:**

   ```bash
   sudo python3 installer_script.py
   ```

   This will copy the `Tor.py` script to the appropriate location and create a command-line utility named `aop`.

## Usage

To start using the Auto IP Changer:

1. **Ensure Tor is Installed and Running:**

   - **Install Tor:**

     On Debian-based systems (e.g., Ubuntu):

     ```bash
     sudo apt update
     sudo apt install tor -y
     ```

     On Red Hat-based systems (e.g., Fedora):

     ```bash
     sudo dnf install tor -y
     ```

     On Arch Linux:

     ```bash
     sudo pacman -S tor
     ```

   - **Start the Tor Service:**

     ```bash
     sudo service tor start
     ```

   - **Verify Tor is Running:**

     Ensure that Tor's SOCKS proxy is listening on `127.0.0.1:9050`. You can check this by running:

     ```bash
     netstat -tnlp | grep 9050
     ```

     You should see an entry indicating that Tor is listening on this port.

2. **Start the Script:**

   ```bash
   aop
   ```

   You will be prompted to enter:
   - **Interval for Changing IP (in seconds):** Default is 60 seconds.
   - **Number of IP Changes:** Default is 1000. Enter 0 for infinite changes.

   The script will start changing your IP address according to your specified interval and number of changes.

3. **Stopping the Script:**

   You can stop the script at any time by pressing `Ctrl+C`.

## Uninstallation

To remove the Auto IP Changer script from your system:

1. **Run the Uninstaller Script:**

   ```bash
   sudo python3 installer_script.py uninstall
   ```

   This will remove the script and command-line utility from your system.

## Dependencies

- **Python 3:** Ensure Python 3 is installed on your system.
- **Python Packages:** `requests`

   Install necessary Python packages using:

   ```bash
   pip3 install requests
   ```

- **Tor:** Ensure Tor is installed and running.

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub]

## Contact

For questions or support, feel free to reach out via GitHub issues


This version includes detailed instructions on installing and configuring Tor, ensuring users know how to get everything set up for the script to work correctly.
