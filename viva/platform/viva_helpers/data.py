from command import Command
from constants import Constants
from logger import Logger
from sql import SQL, Tables

class Data(Command):



  # --------------------------------------------------------------------------------------------------------------------
  # Framework functions
  # --------------------------------------------------------------------------------------------------------------------

  def log(self, level, message, terminal_print=True, write_logs=True):
    Logger(logfile=Logger.VIVA, tag="data", level=level, message=message, terminal_print=terminal_print, write_logs=write_logs)

  def handle_command(self, args):
    rc = self.SUCCESS

    if args.command != "data":
      return self.UNKNOWN_COMMAND

    # Parse args here
    if args.test:
      SQL()

    #else:
    #  self.log(Logger.WARNING, "No arguments were provided.", write_logs=False)
    #  rc |= self.FAILED

    return rc


  def add_arguments(self, common_parser, subparsers):
    epilog = ""
    parser = subparsers.add_parser("data", description="Add, update or remove Viva data.", epilog=epilog, parents=[common_parser])

    parser.add_argument("--test", action="store_true", help="test")

