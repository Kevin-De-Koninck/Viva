from command import Command
from constants import Constants
from logger import Logger
from sql import *

class Data(Command):
  def __init__(self):
    self.sql = SQL()

  def manage_animal(self, args):
    rc = self.SUCCESS

    # Create animal if it does not exist yet
    if not self.sql.query(Animal, name=args.animal):
      self.sql.add_record(Animal(name=args.animal))
    animal_row = self.sql.query(Animal, name=args.animal)

    # Update columns
    if args.home:
      vivarium_row = self.sql.query(Vivarium, name=args.home)
      if vivarium_row:
        animal_row.vivarium_id = vivarium_row.id
      else:
        self.log_animal(Logger.ERROR,"Vivarium '%s' does not exist." % args.home)
        rc |= self.FAILED

    if args.species:
      animal_row.species = args.species
      self.log_animal(Logger.SUCCESS, "Species has been set to '%s'." % args.species)

    if args.morph:
      animal_row.morph = args.morph
      self.log_animal(Logger.SUCCESS, "Morph has been set to '%s'." % args.morph)

    if args.dob:
      animal_row.dob = args.dob
      self.log_animal(Logger.SUCCESS, "DOB has been set to '%s'." % args.dob)

    if args.picture:
      animal_row.picture = args.picture
      self.log_animal(Logger.SUCCESS, "Picture has been set to '%s'." % args.picture)

    return rc

  def manage_vivarium(self, args):
    rc = self.SUCCESS

    # Before creating a new entry, validate everything
    if args.width:
      try:
        width = float(args.width)
      except:
        self.log_vivarium(Logger.ERROR, "Unable to parse the width, '%s' is nat a valid float." % str(args.width))
        rc |= self.FAILED
        width = None

    if args.height:
      try:
        height = float(args.height)
      except:
        self.log_vivarium(Logger.ERROR, "Unable to parse the height, '%s' is nat a valid float." % str(args.height))
        rc |= self.FAILED
        height = None

    if args.depth:
      try:
        depth = float(args.depth)
      except:
        self.log_vivarium(Logger.ERROR, "Unable to parse the depth, '%s' is nat a valid float." % str(args.depth))
        rc |= self.FAILED
        depth = None

    # Create vivarium if it does not exist yet
    if not self.sql.query(Vivarium, name=args.vivarium):
      self.sql.add_record(Vivarium(name=args.vivarium))
    vivarium_row = self.sql.query(Vivarium, name=args.vivarium)

    # Update columns
    if args.picture:
      vivarium_row.picture = args.picture

    if width:
      vivarium_row.width = width
      self.log_vivarium(Logger.SUCCESS, "Width has been set to '%s'." % str(width))

    if height:
      vivarium_row.height = height
      self.log_vivarium(Logger.SUCCESS, "Height has been set to '%s'." % str(height))

    if depth:
      vivarium_row.depth = depth
      self.log_vivarium(Logger.SUCCESS, "Depth has been set to '%s'." % str(depth))

    return rc

  def manage_sensor(self, args):
    rc = self.SUCCESS

    # Before creating a new entry, validate everything
    if not (args.location and args.what and args.value):
      self.log_vivarium(Logger.ERROR, "Not all required arguments were provided (--what/--location/--value).", tag="sensor")
      return self.FAILED

    try:
      value = float(args.value)
    except:
      self.log_vivarium(Logger.ERROR, "Unable to parse the value, '%s' is nat a valid float." % str(args.value))
      rc |= self.FAILED

    vivarium_row = self.sql.query(Vivarium, name=args.sensor)
    if vivarium_row:
      id = vivarium_row.id
    else:
      self.log_vivarium(Logger.ERROR, "Vivarium '%s' does not exist." % args.sensor)
      return self.FAILED

    # Create sensor measurement
    self.sql.add_record(Sensors(vivarium_id=id, what=args.what, location=args.location, value=value))
    self.log_vivarium(Logger.SUCCESS, "Added '%s' measurement (value: '%s') of sensor '%s'." % (args.what, str(args.value), args.location))

    return rc

  def manage_physics(self, args):
    rc = self.SUCCESS

    # Before creating a new entry, validate everything
    if not (args.what and args.value):
      self.log_animal(Logger.ERROR, "Not all required arguments were provided (--what/--value).", tag="physics")
      return self.FAILED

    try:
      value = float(args.value)
    except:
      self.log_animal(Logger.ERROR, "Unable to parse the value, '%s' is nat a valid float." % str(args.value))
      rc |= self.FAILED

    animal_row = self.sql.query(Animal, name=args.physics)
    if animal_row:
      id = animal_row.id
    else:
      self.log_animal(Logger.ERROR, "Animal '%s' does not exist." % args.physics)
      return self.FAILED

    # Create physics entry
    self.sql.add_record(Physics(animal_id=id, what=args.what, value=value))
    self.log_vivarium(Logger.SUCCESS, "Added '%s' measurement (value: '%s')." % (args.what, str(args.value)))

    return rc

  def manage_food(self, args):
    rc = self.SUCCESS

    # Before creating a new entry, validate everything
    animal_row = self.sql.query(Animal, name=args.feedings)
    if animal_row:
      id = animal_row.id
    else:
      self.log_animal(Logger.ERROR, "Animal '%s' does not exist." % args.feedings)
      return self.FAILED

    # Create food entry
    self.sql.add_record(Feedings(animal_id=id, what=args.food, prekilled=args.prekilled, refused=args.refused))
    self.log_vivarium(Logger.SUCCESS, "Added food entry: '%s' (prekilled: '%s', refused: '%s')." % (args.food, str(args.prekilled), str(args.refused)))

    return rc









  # --------------------------------------------------------------------------------------------------------------------
  # Framework functions
  # --------------------------------------------------------------------------------------------------------------------

  def log_vivarium(self, level, message, terminal_print=True, write_logs=True, tag="vivarium"):
    Logger(logfile=Logger.TERRARIUM, tag=tag, level=level, message=message, terminal_print=terminal_print, write_logs=write_logs)

  def log_animal(self, level, message, terminal_print=True, write_logs=True, tag="animal"):
    Logger(logfile=Logger.REPTILE, tag=tag, level=level, message=message, terminal_print=terminal_print, write_logs=write_logs)

  def log_system(self, level, message, terminal_print=True, write_logs=True):
    Logger(logfile=Logger.VIVA, tag="data/SQL", level=level, message=message, terminal_print=terminal_print, write_logs=write_logs)

  def handle_command(self, args):
    rc = self.SUCCESS

    if args.command != "data":
      return self.UNKNOWN_COMMAND

    if args.animal:
      rc |= self.manage_animal(args)
    elif args.vivarium:
      rc |= self.manage_vivarium(args)
    elif args.sensor:
      rc |= self.manage_sensor(args)
    elif args.physics:
      rc |= self.manage_physics(args)
    elif args.feedings:
      rc |= self.manage_food(args)

    else:
      self.log_system(Logger.WARNING, "No arguments were provided.", write_logs=False)
      rc |= self.FAILED

    self.sql.save()
    return rc


  def add_arguments(self, common_parser, subparsers):
    epilog = ""
    parser = subparsers.add_parser("data", description="Add, update or remove Viva data.", epilog=epilog, parents=[common_parser])

    #  TODO: ADD '--modify ID' to modify stuff like food and physics

    # Animal: name, vivarium, species, morph, dob, picture
    parser.add_argument("--animal", metavar="NAME", help="Add an animal to the database, or update if it already exists")
    parser.add_argument("--home", metavar="NAME", help="Assign/update the animal's home (vivarium must exist, add it first)")
    parser.add_argument("--species", metavar="SPECIES", help="Assign/update a species to the animal")
    parser.add_argument("--morph", metavar="NAME", help="Assign/update the morph of the animal")
    parser.add_argument("--dob", metavar="DOB", help="Assign/update the DOB ('yyyy/mm/dd')")
    parser.add_argument("--picture", metavar="NAME", help="Assign/update the picture")

    # Vivarium: name, width, height, depth, picture
    parser.add_argument("--vivarium", metavar="NAME", help="Add a vivarium to the database, or update if it already exists")
    parser.add_argument("--height", metavar="FLOAT", help="Assign/update the height of the vivarium")
    parser.add_argument("--width", metavar="FLOAT", help="Assign/update the width of the vivarium")
    parser.add_argument("--depth", metavar="FLOAT", help="Assign/update the depth of the vivarium")

    # Sensors: vivarium_name, what, location, value
    parser.add_argument("--sensor", metavar="VIVARIUM_NAME", help="Add a sensor measurement to the database for the given vivarium name")
    parser.add_argument("--what", metavar="WHAT", help="Assign what was measured (e.g. 'Temperature', 'Body weight', ...)")
    parser.add_argument("--location", metavar="SENSOR_NAME", help="Assign the location of the measurement in the vivarium")
    parser.add_argument("--value", metavar="FLOAT", help="Assign/update the value")

    # Physics: animal_id, what, value
    parser.add_argument("--physics", metavar="ANIMAL_NAME", help="Add a body measurement of the animal")

    # Feedings: animal_id, what, prekilled, refused
    parser.add_argument("--feedings", metavar="ANIMAL_NAME", help="Add a mealtime for the animal")
    parser.add_argument("--food", metavar="WHAT", help="Assign what was eaten (e.g. 'Adult rat')")
    parser.add_argument("--prekilled", action="store_true", help="The diner was prekilled instead of alive")
    parser.add_argument("--refused", action="store_true", help="The animal refused to eat")





