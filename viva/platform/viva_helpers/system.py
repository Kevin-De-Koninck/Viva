from logger import Logger
from command import Command


class System(Command):

  def install_or_update_all(self):
    return self.SUCCESS

  def install_or_update_nginx(self):
    return self.SUCCESS

  def install_or_update_mysql(self):
    return self.SUCCESS

  def install_or_update_viva_framework(self):
    return self.SUCCESS

  def install_or_update_viva_website(self):
    return self.SUCCESS

  def system_update(self):
    return self.SUCCESS



  # --------------------------------------------------------------------------------------------------------------------
  # Framework functions
  # --------------------------------------------------------------------------------------------------------------------

  def log(self, level, message, terminal_print=True):
    Logger(logfile=Logger.VIVA, tag="system", level=level, message=message, terminal_print=terminal_print)

  def handle_command(self, args):
    rc = self.SUCCESS

    if args.command != "system":
      return self.UNKNOWN_COMMAND

    if args.all:
      rc |= self.install_or_update_all()

    elif args.nginx or args.mysql or args.viva_framework or args.viva_website or args.system_update:
      if args.nginx:
        rc |= self.install_or_update_nginx()
      if args.mysql:
        rc |= self.install_or_update_mysql()
      if args.viva_framework:
        rc |= self.install_or_update_viva_framework()
      if args.viva_website:
        rc |= self.install_or_update_viva_website()
      if args.nginx:
        rc |= self.system_update()

    else:
      self.log(Logger.WARNING, "No arguments were provided.")
      rc |= self.FAILED

    return rc


  def add_arguments(self, common_parser, subparsers):
    epilog = ""
    parser = subparsers.add_parser("system", description="Install and/or update Viva.", epilog=epilog, parents=[common_parser])

    parser.add_argument("--all", action="store_true", help="Install and/or update viva and the system completely")

    parser.add_argument("--nginx", action="store_true", help="Install and/or update NGINX")
    parser.add_argument("--mysql", action="store_true", help="Install and/or update MySQL")
    parser.add_argument("--viva-framework", action="store_true", help="Update the viva command")
    parser.add_argument("--viva-website", action="store_true", help="Install and/or update the viva website pages")

    parser.add_argument("--system-update", action="store_true", help="Update the OS packages and python packages")
