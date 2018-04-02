from command import Command
from constants import Constants
from logger import Logger
from sql import *

class Data(Command):
  def __init__(self):
    self.sql = SQL()

  def manage_animal(self, args):
    rc = self.SUCCESS

    # TODO also delete all rows with animal ID  in shedding, note, physics, food
    if args.delete:
      if not self.sql.query(Animal, id=args.delete):
        self.log_animal(Logger.WARNING, "There is no animal with ID '%s'." % str(args.delete))
      else:
        try:
          self.sql.delete_record_by_ID(Animal, int(args.delete))
          self.log_animal(Logger.SUCCESS, "Animal with ID '%s' has been deleted." % str(args.delete))
          return self.SUCCESS
        except Exception as e:
          self.log_animal(Logger.ERROR, "Failed to remove row with ID '%s'." % str(args.delete))
          return self.FAILED

    # Create animal if it does not exist yet
    if not self.sql.query(Animal, name=args.name):
      self.sql.add_record(Animal(name=args.name))
    animal_row = self.sql.query(Animal, name=args.name)

    # Update columns
    if args.vivarium:
      rc_, id = self.get_vivarium_id(args.vivarium)
      if rc_ == self.FAILED:
        return rc_
      animal_row.vivarium_id = id

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

    if args.new_name:
      animal_row.name = args.new_name
      self.log_animal(Logger.SUCCESS, "Name has been set to '%s'." % args.new_name)

    return rc

  def manage_vivarium(self, args):
    rc = self.SUCCESS

    # TODO also delete all rows with animal ID  in settings, sensors
    if args.delete:
      if not self.sql.query(Vivarium, id=args.delete):
        self.log_animal(Logger.WARNING, "There is no vivarium with ID '%s'." % str(args.delete))
      else:
        try:
          self.sql.delete_record_by_ID(Vivarium, int(args.delete))
          self.log_animal(Logger.SUCCESS, "Vivarium with ID '%s' has been deleted." % str(args.delete))
          return self.SUCCESS
        except Exception as e:
          self.log_animal(Logger.ERROR, "Failed to remove row with ID '%s'." % str(args.delete))
          return self.FAILED

    # Before creating a new entry, validate everything
    if args.width:
      try:
        width = float(args.width)
      except:
        self.log_vivarium(Logger.ERROR, "Unable to parse the width, '%s' is nat a valid float." % str(args.width))
        rc |= self.FAILED
        width = None
    else:
      width = None

    if args.height:
      try:
        height = float(args.height)
      except:
        self.log_vivarium(Logger.ERROR, "Unable to parse the height, '%s' is nat a valid float." % str(args.height))
        rc |= self.FAILED
        height = None
    else:
      height = None

    if args.depth:
      try:
        depth = float(args.depth)
      except:
        self.log_vivarium(Logger.ERROR, "Unable to parse the depth, '%s' is nat a valid float." % str(args.depth))
        rc |= self.FAILED
        depth = None
    else:
      depth = None

    # Create vivarium if it does not exist yet
    if not self.sql.query(Vivarium, name=args.name):
      self.sql.add_record(Vivarium(name=args.name))
    vivarium_row = self.sql.query(Vivarium, name=args.name)

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

    if args.new_name:
      vivarium_row.name = args.new_name
      self.log_animal(Logger.SUCCESS, "Name has been set to '%s'." % args.new_name)

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

    rc_, id = self.get_vivarium_id(args.vivarium)
    if rc_ == self.FAILED:
      return rc_

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

    rc_, id = self.get_animal_id(args.physics)
    if rc_ == self.FAILED:
      return rc_

    # Create physics entry
    self.sql.add_record(Physics(animal_id=id, what=args.what, value=value))
    self.log_vivarium(Logger.SUCCESS, "Added '%s' measurement (value: '%s')." % (args.what, str(args.value)))

    return rc

  def manage_food(self, args):
    rc = self.SUCCESS

    # Before creating a new entry, validate everything
    rc_, id = self.get_animal_id(args.feedings)
    if rc_ == self.FAILED:
      return rc_

    # Create food entry
    self.sql.add_record(Feedings(animal_id=id, what=args.food, prekilled=args.prekilled, refused=args.refused))
    self.log_vivarium(Logger.SUCCESS, "Added food entry: '%s' (prekilled: '%s', refused: '%s')." % (args.food, str(args.prekilled), str(args.refused)))

    return rc

  def manage_note(self, args):
    rc = self.SUCCESS

    # Before creating a new entry, validate everything
    rc_, id = self.get_animal_id(args.note)
    if rc_ == self.FAILED:
      return rc_

    # Create note entry
    self.sql.add_record(Notes(animal_id=id, note=args.text))
    self.log_vivarium(Logger.SUCCESS, "Added note for animal '%s'." % args.note)

    return rc

  def manage_shedding(self, args):
    rc = self.SUCCESS

    # Before creating a new entry, validate everything
    rc_, id = self.get_animal_id(args.shedding)
    if rc_ == self.FAILED:
      return rc_

    # Create note entry
    self.sql.add_record(Sheddings(animal_id=id, note=args.text, successful=args.successful))
    self.log_vivarium(Logger.SUCCESS, "Added a shedding entry for animal '%s' (successful shedding: '%s')." % (args.shedding, str(args.successful)))

    return rc

  def get_animal_id(self, animal):
    row = self.sql.query(Animal, name=animal)
    if row:
      return self.SUCCESS, row.id
    else:
      self.log_animal(Logger.ERROR, "Animal '%s' does not exist." % animal)
      return self.FAILED, None

  def get_vivarium_id(self, vivarium):
    row = self.sql.query(Vivarium, name=vivarium)
    if row:
      return self.SUCCESS, row.id
    else:
      self.log_animal(Logger.ERROR, "Vivarium '%s' does not exist." % vivarium)
      return self.FAILED, None




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

    if args.command not in  ["data", "animal", "vivarium", "sensor", "physics", "food", "note", "shedding"]:
      return self.UNKNOWN_COMMAND

    if args.command == "animal":
      rc |= self.manage_animal(args)

    if args.command == "vivarium":
      rc |= self.manage_vivarium(args)

    if args.command == "sensor":
      rc |= self.manage_sensor(args)

    if args.command == "physics":
      rc |= self.manage_physics(args)

    if args.command == "food":
      rc |= self.manage_food(args)

    if args.command == "note":
      rc |= self.manage_note(args)

    if args.command == "shedding":
      rc |= self.manage_shedding(args)

    self.sql.save()
    return rc


  def add_arguments(self, common_parser, subparsers):
    #  TODO: ADD '--modify ID' to modify stuff like food and physics
    # to modify stuff
    #parser.add_argument("--modify", metavar="ID", help="The ID of the row that we want to modify")
    #parser.add_argument("--delete", metavar="ID", help="The ID of the row that we want to delete")


    animal_parser = subparsers.add_parser("animal", description="Add, update or remove an animal.", parents=[common_parser])
    # Animal: name, vivarium, species, morph, dob, picture
    animal_parser.add_argument("--name", metavar="NAME", help="Name of the animal")
    animal_parser.add_argument("--new-name", metavar="NAME", help="New name of the animal")
    animal_parser.add_argument("--vivarium", metavar="NAME", help="Assign/update the animal's home (vivarium must exist, add it first)")
    animal_parser.add_argument("--species", metavar="SPECIES", help="Assign/update a species to the animal")
    animal_parser.add_argument("--morph", metavar="NAME", help="Assign/update the morph of the animal")
    animal_parser.add_argument("--dob", metavar="DOB", help="Assign/update the DOB ('yyyy/mm/dd')")
    animal_parser.add_argument("--picture", metavar="NAME", help="Assign/update the picture")
    animal_parser.add_argument("--delete", metavar="ID", help="The ID of the row that we want to delete")

    vivarium_parser = subparsers.add_parser("vivarium", description="Add, update or remove a vivarium.", parents=[common_parser])
    # Vivarium: name, width, height, depth, picture
    vivarium_parser.add_argument("--name", metavar="NAME", help="Name of the vivarium")
    vivarium_parser.add_argument("--new-name", metavar="NAME", help="New name of the vivarium")
    vivarium_parser.add_argument("--height", metavar="FLOAT", help="Assign/update the height of the vivarium")
    vivarium_parser.add_argument("--width", metavar="FLOAT", help="Assign/update the width of the vivarium")
    vivarium_parser.add_argument("--depth", metavar="FLOAT", help="Assign/update the depth of the vivarium")
    vivarium_parser.add_argument("--picture", metavar="NAME", help="Assign/update the picture")
    vivarium_parser.add_argument("--delete", metavar="ID", help="The ID of the row that we want to delete")

    sensor_parser = subparsers.add_parser("sensor", description="Add, update or remove a sensor measurement.", parents=[common_parser])
    # Sensors: vivarium_name, what, location, value
    sensor_parser.add_argument("--vivarium", metavar="NAME", help="Vivarium name of the sensor's location")
    sensor_parser.add_argument("--what", metavar="WHAT", help="Assign what was measured (e.g. 'Temperature')")
    sensor_parser.add_argument("--location", metavar="SENSOR_NAME", help="Assign the location of the measurement in the vivarium")
    sensor_parser.add_argument("--value", metavar="FLOAT", help="Assign/update the value")

    physics_parser = subparsers.add_parser("physics", description="Add, update or remove an animal measurement.", parents=[common_parser])
    # Physics: animal_id, what, value
    physics_parser.add_argument("--animal", metavar="NAME", help="Name of the animal")
    physics_parser.add_argument("--what", metavar="WHAT", help="Assign what was measured (e.g. 'Body weight')")
    physics_parser.add_argument("--value", metavar="FLOAT", help="Assign/update the value")

    food_parser = subparsers.add_parser("food", description="Add, update or remove a mealtime.", parents=[common_parser])
    # Feedings: animal_id, what, prekilled, refused
    food_parser.add_argument("--animal", metavar="NAME", help="Name of the animal")
    food_parser.add_argument("--food", metavar="WHAT", help="Assign what was eaten (e.g. 'Adult rat')")
    food_parser.add_argument("--prekilled", action="store_true", help="The diner was prekilled instead of alive")
    food_parser.add_argument("--refused", action="store_true", help="The animal refused to eat")

    note_parser = subparsers.add_parser("note", description="Add, update or remove a note for an animal.", parents=[common_parser])
    # Note: animal_id, note
    note_parser.add_argument("--animal", metavar="NAME", help="Name of the animal")
    note_parser.add_argument("--note", metavar="WHAT", help="The text of the note")

    shedding_parser = subparsers.add_parser("shedding", description="Add, update or remove a shedding entry.", parents=[common_parser])
    # Shedding: animal_id, note, successfull
    shedding_parser.add_argument("--shedding", metavar="ANIMAL_NAME", help="Add a shedding entry for the animal")
    shedding_parser.add_argument("--note", metavar="WHAT", help="An optional note")
    shedding_parser.add_argument("--successful", action="store_true", help="The shedding was successful")






