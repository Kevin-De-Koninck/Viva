import subprocess
from logger import Logger
from helpers import Namespace



class Command:
  SUCCESS = 0
  FAILED = 1
  UNKNOWN_COMMAND = -1

  # usage: excecute("ls", "-l")
  #        execute("ls -l")
  # or     execute(["ls", "-l"])
  @staticmethod
  def execute(*command, **kwargs):
    shell = kwargs.pop('shell', False)
    Logger(Logger.VIVA, "system", Logger.INFO, "Executing command: %s" % str(" ".join(command)), terminal_print=True)

    # Check type of arguments passed and parse to list
    if type(command[0]) == type(str()):
      if " " in command[0]:
        command = command[0].split()
      else:
        command = list(command)
    elif type(command[0]) == type(list()):
      command = command[0]
    else:
      result = Namespace(rc=1, output="Error parsing the command, wrong arguments were provided...", succeeded=False, failed=True)
      Logger(logfile=Logger.VIVA, tag="system", level=Logger.ERROR, message=result.output)
      return result

    try:
      # Get stdout and stderr
      output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=shell)
      rc = 0

    # If the executed command returns a nonzero exit code, an exception is raised
    except subprocess.CalledProcessError as e:
      output = e.output  # Output generated before error
      rc = e.returncode  # Return code

    cmd_result = Namespace(rc=rc, output=output, succeeded=True if not rc else False, failed=True if rc else False)
    if cmd_result.failed:
      Logger(logfile=Logger.VIVA, tag="system", level=Logger.ERROR, message=cmd_result.output)

    return cmd_result
