import os

class Constants:
  class Viva:
    GROUP = "viva"
    USER = "viva"

  class Paths:
    LOG_DIR = "/var/log/viva"
    LOG_TERRARIUM = os.path.join(LOG_DIR, "terrarium.log")
    LOG_REPTILE = os.path.join(LOG_DIR, "reptile.log")
    LOG_VIVA = os.path.join(LOG_DIR, "viva.log")