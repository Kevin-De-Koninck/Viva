import os
import sys
import pwd
import grp
from datetime import datetime

from constants import Constants


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

  REPTILE = Constants.Paths.LOG_REPTILE
  TERRARIUM = Constants.Paths.LOG_TERRARIUM
  VIVA = Constants.Paths.LOG_VIVA

  def __init__(self, logfile, tag, level, message):
    self.level = level if level in [self.ERROR, self.WARNING, self.SUCCESS, self.INFO] else self.INFO
    self.message = message
    self.logfile = logfile if logfile in [self.REPTILE, self.VIVA, self.TERRARIUM] else self.VIVA
    self.tag = str(tag)

    self.terminal_print()
    self.write_logs()

  def terminal_print(self):
    message = "[%s] %s" % (str(self.level), str(self.message))
    if os.isatty(sys.stdout.fileno()):
      print self.set_color() + message + PrintColors.END
    else:
      print str(message)

  def set_color(self):
    if self.level == self.ERROR:
      return PrintColors.ERROR
    elif self.level == self.WARNING:
      return PrintColors.WARNING
    elif self.level == self.SUCCESS:
      return PrintColors.SUCCESS
    else:
      return PrintColors.INFO

  def write_logs(self):
    # "2018-03-25 14:54:32.58 MySQL: [INFO] Updated table R_Diablo with new weight info: 2018-03-15; 8kg"
    log_msg = "%s %s: [%s] %s" % (str(datetime.now())[:-4], self.tag, str(self.level), self.message.replace('"','').replace("'",''))

    if not os.path.isdir(Constants.Paths.LOG_DIR):
      os.mkdir(Constants.Paths.LOG_DIR, 0755)  #RW R R

    with open(self.logfile, 'a+') as f:
      f.write("%s\n" % log_msg)

    # Set correct user and group (not root:root but viva:viva)
    uid = pwd.getpwnam(Constants.Viva.USER).pw_uid
    gid = grp.getgrnam(Constants.Viva.GROUP).gr_gid
    os.chown(Constants.Paths.LOG_DIR, uid, gid)
    os.chown(self.logfile, uid, gid)
    os.chmod(self.logfile, 0644)
    os.chmod(Constants.Paths.LOG_DIR, 0755)


