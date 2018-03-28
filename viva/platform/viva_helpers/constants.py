import os

class Constants:
  class Viva:
    GROUP = "viva"
    USER = "viva"

  class LEMP:
    MYSQL_ROOT_PWD = "VivaMySQL"


  class Paths:
    OPT_DIR = "/opt/viva"
    BASH_SCRIPTS_DIR = os.path.join(OPT_DIR, "bash_scripts")
    LOG_DIR = "/var/log/viva"
    LOG_TERRARIUM = os.path.join(LOG_DIR, "terrarium.log")
    LOG_REPTILE = os.path.join(LOG_DIR, "reptile.log")
    LOG_VIVA = os.path.join(LOG_DIR, "viva.log")