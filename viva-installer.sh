#!/bin/bash

# ----------------------------
# Constants
# ----------------------------

INSTALL_LOCATION="/opt/viva"                          # Viva install location
REPO="https://github.com/Kevin-De-Koninck/Viva.git"   # Repository name

VIVA_USER="viva"                                      # To create user
VIVA_GROUP="viva"                                     # To create group
VIVA_PASSWORD="viva"                                  # User password


# ----------------------------
# Functions
# ----------------------------

function check_root() {
  if [ "$EUID" -ne 0 ]
    then echo "Please run as root or use sudo..."
    exit 1
  fi
}

function apt_enable_progress_bar() {
  echo 'Dpkg::Progress-Fancy "1";' > /etc/apt/apt.conf.d/99progressbar
}

function create_user_and_group() {
  if ! id -u vivaa &> /dev/null; then                             # Only is user does not exist
    useradd ${VIVA_USER} --shell /bin/bash --create-home          # Create user
    echo "${VIVA_USER}:${VIVA_PASSWORD}" | chpasswd               # Modify password
    usermod --append -G ${VIVA_GROUP} ${VIVA_USER}                # Add user to group
    echo "${VIVA_GROUP} ALL=(ALL) NOPASSWD: ALL" | EDITOR='tee -a' visudo   # Add group to sudoers (allow root access)
  fi
}

function install_packages() {
  apt install -y git python python-pip
  export LC_ALL=C
  pip install -y ipdb
}

function install_viva() {
  temp_dir=$(mktemp -d)                                    # Create temp folder
  git clone ${REPO} ${temp_dir}                            # Clone repo in temp folder
  mkdir -p ${INSTALL_LOCATION}                             # Make sure the install location exists
  cp -r ${temp_dir}/viva/platform/* ${INSTALL_LOCATION}    # Copy some files to the install location
  chown -R ${VIVA_USER}:${VIVA_GROUP} ${INSTALL_LOCATION}  # Change the owner
  chmod -R 755 ${INSTALL_LOCATION}                         # Set permissions
  echo "export 'PATH=${PATH}:${INSTALL_LOCATION}:${INSTALL_LOCATION}/bash_scripts'" >> /home/${VIVA_USER}/.bashrc # Make command available
}

function fix_locale_ssh_warnings() {
  locale-gen en_US.UTF-8
  sed -i '/LANG LC_*/d' /etc/ssh/ssh_config
  sed -i '/LANG LC_*/d' /etc/ssh/sshd_config
  update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
  service ssh reload

}


# ----------------------------
# Installer
# ----------------------------

# Check if root
check_root

# Enable a fancy progress bar when using apt
apt_enable_progress_bar

# solve some anoying errors that start with 'perl: warning: Setting locale failed.'
fix_locale_ssh_warnings

# Create the new user and group and assign root access
create_user_and_group

# Install Viva with the required packages
install_packages
install_viva

# log out, user should use 'Viva' now instead of root
clear
echo "1. Viva has been installed on your system."
echo "2. User '${VIVA_USER}' has been created with sudo permissions."
echo "3. Continue as user '${VIVA_USER}' and start the installation using 'viva install'."
echo
echo "The script will nog log you out, please log back in as user '${VIVA_USER}'."
read -n 1 -s -r -p "Press any key to continue..."
logout
