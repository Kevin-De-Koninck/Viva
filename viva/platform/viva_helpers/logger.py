import os
import sys


class PrintColors:
  ERROR = '\033[91m'  # Red
  WARNING = '\033[93m'  # Yellow
  SUCCESS = '\033[92m'  # Green
  INFO = '\033[94m'  # Blue
  END = '\033[0m'


class Logger:
  ERROR = "ERROR"
  WARNING = "WARNING"
  SUCCESS = "SUCCESS"
  INFO = "INFO"

  def __init__(self, level, message):
    self.level = level if level in [self.ERROR, self.WARNING, self.SUCCESS, self.INFO] else self.INFO
    self.message = self.prepare_message(message)
    self.color_print()

  def prepare_message(self, message):
    return "[%s] %s" % (str(self.level), str(message))

  def color_print(self):
    if os.isatty(sys.stdout.fileno()):
      print self.set_color() + self.message + PrintColors.END
    else:
      print str(self.message)

  def set_color(self):
    if self.level == self.ERROR:
      return PrintColors.ERROR
    elif self.level == self.WARNING:
      return PrintColors.WARNING
    elif self.level == self.SUCCESS:
      return PrintColors.SUCCESS
    else:
      return PrintColors.INFO
