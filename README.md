# Viva

Viva is a platform on which you can monitor and control all your terraria and vivaria at once. The sensors and actors are physically separated from the backend to ensure optimal and fail safe operations.
The backend can run in a VM based on Alpine Linux or or, later, in a Docker container.


## Operating system

Viva is developed for [Ubuntu Server 16.04.4 LTS](https://www.ubuntu.com/download/server) and will later be converted to
Alpine Linux inside a Docker container. Other operating systems are not officially supported but Viva should be pretty cross-OS. E.g. I see no problem to install Viva on e.g. a Raspberry Pi.

1. Install Ubuntu Server
    - username is free to choose
    - Make sure you have internet access
    - set up a static IP address (!)
    - Install security updates automatically
    - Install standard system utilities
    - Install GRUB bootloader to the master boot record
2. If your keyboard layout is not correct: `sudo dpkg-reconfigure keyboard-configuration`
3. Update your system: `sudo apt update && sudo apt upgrade -y`
4. Make your system SSH ready: `sudo apt install -y openssh-server`
5. If you did not set up a static IP address in the installer, follow [this guide](https://askubuntu.com/a/470245) to set one up.
6. Get your IP address: `hostname -I`
7. SSH into your server: `ssh USER@IP_ADDR`


## Install Viva

The Viva installer will configure a viva user (and delete an existing one first). It will also install the viva command:
```
cd $(mktemp -d)
wget https://raw.githubusercontent.com/Kevin-De-Koninck/Viva/master/viva-installer.sh
chmod +x viva-installer.sh
./viva-installer.sh
```

Now log in as user 'viva' and use the viva command to start the installation of the webserver, mySQL, ...:
```
viva install
``
