import os
from constants import Constants
from logger import Logger
from command import Command
from config_files import Unattended_upgrades, NginX


class System(Command):

  def install_or_update_all(self):
    rc = self.SUCCESS
    rc |= self.enable_automatic_upgrades()
    rc |= self.update_packages()
    rc |= self.install_or_update_LEMP()
    return rc

  def install_or_update_LEMP(self, args):
    # Set the root password for unattended install of MySQL
    os.system('echo "mysql-server mysql-server/root_password password %s" | debconf-set-selections' % str(Constants.LEMP.MYSQL_ROOT_PWD))
    os.system('echo "mysql-server mysql-server/root_password_again password %s" | debconf-set-selections' % str(Constants.LEMP.MYSQL_ROOT_PWD))

    # Install MySQL
    if self.execute("apt install -y mysql-server php-mysql libmysqlclient-dev").failed:
      return self.FAILED
    self.log(Logger.SUCCESS, "Successfully installed/updated MySQL.")

    # Install NginX
    for command in ["apt install -y nginx", "service nginx start"]:
      if self.execute(command).failed:
        return self.FAILED
    self.log(Logger.SUCCESS, "Successfully installed/updated NginX.")

    # Install PHP
    if self.execute("apt install -y php-fpm").failed:
      return self.FAILED
    self.log(Logger.SUCCESS, "Successfully installed/updated PHP.")

    # Configure NginX
    if self.execute("mv %(file)s %(file)s.backup" % {'file': NginX.sites_available_default.filename}).failed:
      return self.FAILED

    try:
      with open(NginX.sites_available_default.filename, "w+") as f:
        f.write(NginX.sites_available_default.content)
    except Exception as e:
      self.log(Logger.ERROR, "An error occurred while writing to '%s': %s" % (NginX.sites_available_default.filename, str(e)))
      return self.FAILED

    if self.execute("adduser %s www-data" % Constants.Viva.USER).failed:
      return self.FAILED
    if self.execute("chown %s:www-data -R /usr/share/nginx/" % Constants.Viva.USER).failed:
      return self.FAILED

    self.log(Logger.SUCCESS, "Successfully configured NginX.")

    # Install PHPMyAdmin
    for command in ['echo "phpmyadmin phpmyadmin/dbconfig-install boolean true" | debconf-set-selections',
                    'echo "phpmyadmin phpmyadmin/app-password-confirm password %s" | debconf-set-selections' % str(Constants.LEMP.MYSQL_ROOT_PWD),
                    'echo "phpmyadmin phpmyadmin/mysql/admin-pass password %s" | debconf-set-selections' % str(Constants.LEMP.MYSQL_ROOT_PWD),
                    'echo "phpmyadmin phpmyadmin/mysql/app-pass password %s" | debconf-set-selections' % str(Constants.LEMP.MYSQL_ROOT_PWD),
                    'echo "phpmyadmin phpmyadmin/reconfigure-webserver multiselect" | debconf-set-selections']:
      os.system(command)

    for command in ["sudo apt install -y phpmyadmin", "service nginx reload", "service php7.0-fpm restart"]:
      if self.execute(command).failed:
        return self.FAILED

    self.log(Logger.SUCCESS, "Successfully installed/configured PHPMyAdmin.")

    # set an info page
    os.system('echo "<?php phpinfo(); ?>" > /usr/share/nginx/html/info.php')

    # DONE
    self.log(Logger.SUCCESS, "Successfully installed/updated LEMP (PHPMyAdmin on port %d)." % NginX.sites_available_default.PHPMyAdmin_port)






    return self.SUCCESS

  def install_or_update_viva_framework(self):
    return self.SUCCESS

  def install_or_update_viva_website(self):
    return self.SUCCESS

  def update_packages(self):
    rc = self.SUCCESS

    for command in ["apt update", "apt upgrade -y", "apt dist-upgrade -y", "apt autoclean", "apt autoremove -y"]:
      if self.execute(command).failed:
        rc |=  self.FAILED
    if rc == self.SUCCESS:
      self.log(Logger.SUCCESS, "Successfully updated the OS packages.")

    if self.execute(os.path.join(Constants.Paths.BASH_SCRIPTS_DIR, "pip_upgrade_all")).failed:
      rc |=  self.FAILED
    else:
      self.log(Logger.SUCCESS, "Successfully updated the Python packages.")

    return rc

  def enable_automatic_upgrades(self):
    if self.execute("apt", "install", "-y" ,"unattended-upgrades").failed:
      return self.FAILED

    for config_file in [Unattended_upgrades.Unattended_upgrades, Unattended_upgrades.Auto_upgrades]:
      try:
        with open(config_file.filename, "w+") as f:
          f.write(config_file.content)
      except Exception as e:
        self.log(Logger.ERROR, "An error occurred while writing to '%s': %s" % (config_file.filename, str(e)))
        return self.FAILED

    self.log(Logger.SUCCESS, "Successfully configured automatic system upgrades.")
    return self.SUCCESS




  # --------------------------------------------------------------------------------------------------------------------
  # Framework functions
  # --------------------------------------------------------------------------------------------------------------------

  def log(self, level, message, terminal_print=True, write_logs=True):
    Logger(logfile=Logger.VIVA, tag="system", level=level, message=message, terminal_print=terminal_print, write_logs=write_logs)

  def handle_command(self, args):
    rc = self.SUCCESS

    if args.command != "system":
      return self.UNKNOWN_COMMAND

    if args.all:
      rc |= self.install_or_update_all()

    elif args.LEMP or args.viva_framework or args.viva_website or args.update_packages or args.enable_automatic_upgrades:
      if args.LEMP:
        rc |= self.install_or_update_LEMP(args)
      if args.viva_framework:
        rc |= self.install_or_update_viva_framework()
      if args.viva_website:
        rc |= self.install_or_update_viva_website()
      if args.update_packages:
        rc |= self.update_packages()
      if args.enable_automatic_upgrades:
        rc |= self.enable_automatic_upgrades()

    else:
      self.log(Logger.WARNING, "No arguments were provided.", write_logs=False)
      rc |= self.FAILED

    return rc


  def add_arguments(self, common_parser, subparsers):
    epilog = ""
    parser = subparsers.add_parser("system", description="Install and/or update Viva.", epilog=epilog, parents=[common_parser])

    parser.add_argument("--all", action="store_true", help="Install and/or update viva and the system completely")

    parser.add_argument("--LEMP", action="store_true", help="Install and/or update NginX, MySQL and PHP")
    parser.add_argument("--viva-framework", action="store_true", help="Update the viva command")
    parser.add_argument("--viva-website", action="store_true", help="Install and/or update the viva website pages")

    parser.add_argument("--update-packages", action="store_true", help="Update the OS packages and python packages")
    parser.add_argument("--enable-automatic-upgrades", action="store_true", help="Enable automatic system upgrades")
