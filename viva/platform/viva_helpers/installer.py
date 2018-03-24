from constants import RC
from logger import Logger


class Install:
  def handle_command(self, args):
    if args.command != "install":
      return RC.UNKNOWN_COMMAND

    if args.test:
      Logger(Logger.INFO, "WOOHOOOOOOO")


  def add_arguments(self, common_parser, subparsers):
    # vdcm-configure user
    epilog = ""
    parser = subparsers.add_parser("install",
                                    description="Configure the vDCM's default user configuration.",
                                    epilog=epilog, parents=[common_parser])

    parser.add_argument("--test", action="store_true", help="Test the framework")
