import subprocess
from logger import Logger

class Command:
  SUCCESS = 0
  FAILED = 1
  UNKNOWN_COMMAND = -1


  # usage: excecute("ls", "-l")
  @staticmethod
  def execute(*command):
    Logger(Logger.VIVA, "system", Logger.INFO, "Now executing command: %s" % str(" ".join(command)), terminal_print=False)
    try:
      # Get stdout and stderr
      output = subprocess.check_output(list(command), stderr=subprocess.STDOUT)
      rc = 0

    # If the executed command returns a nonzero exit code, an exception is raised
    except subprocess.CalledProcessError as e:
      output = e.output  # Output generated before error
      rc = e.returncode  # Return code

    return rc, output
