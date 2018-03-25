from logger import Logger
from command import Command


class Install(Command):
  def log(self, level, message):
    Logger(logfile=Logger.VIVA, tag="install", level=level, message=message)

  def handle_command(self, args):
    if args.command != "install":
      return self.UNKNOWN_COMMAND

    if args.test:
      self.log(Logger.INFO, "WOOHOOOOOOO")


  def add_arguments(self, common_parser, subparsers):
    # vdcm-configure user
    epilog = ""
    parser = subparsers.add_parser("install",
                                    description="Install viva.",
                                    epilog=epilog, parents=[common_parser])

    parser.add_argument("--test", action="store_true", help="Test the framework")
