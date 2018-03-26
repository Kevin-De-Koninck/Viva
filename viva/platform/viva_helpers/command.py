import subprocess

class Command:
  SUCCESS = 0
  FAILED = 1
  UNKNOWN_COMMAND = -1


  # usage: excecute("ls", "-l")
  @staticmethod
  def execute(*command):
    try:
      # Get stdout and stderr
      output = subprocess.check_output(list(command), stderr=subprocess.STDOUT)
      rc = 0

    # If the executed command returns a nonzero exit code, an exception is raised
    except subprocess.CalledProcessError as e:
      output = e.output  # Output generated before error
      rc = e.returncode  # Return code

    return rc, output
