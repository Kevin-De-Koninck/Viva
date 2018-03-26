class Unattended_upgrades:
  class Unattended_upgrades:
    filename = "/etc/apt/apt.conf.d/50unattended-upgrades"
    content = """
Unattended-Upgrade::Allowed-Origins {
        "${distro_id}:${distro_codename}";
        "${distro_id}:${distro_codename}-security";
        "${distro_id}ESM:${distro_codename}";
};

Unattended-Upgrade::Package-Blacklist {
};

Unattended-Upgrade::Automatic-Reboot "false";
Unattended-Upgrade::Automatic-Reboot-Time "02:00";
"""

  class Auto_upgrades:
    filename = "/etc/apt/apt.conf.d/20auto-upgrades"
    content = """
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
APT::Periodic::AutocleanInterval "3";
APT::Periodic::Download-Upgradeable-Packages "1";
"""
