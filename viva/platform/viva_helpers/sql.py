from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, DateTime, Float, Boolean
from sqlalchemy import MetaData, Table

from logger import Logger
from constants import Constants


# Based on https://www.dangtrinh.com/2013/06/sqlalchemy-python-module-with-mysql.html
# ... and https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
class SQL:

  def __init__(self):
    self.username = Constants.LEMP.MYSQL_USERNAME
    self.password = Constants.LEMP.MYSQL_PWD
    self.port = Constants.LEMP.MYSQL_PORT
    self.db_name = Constants.LEMP.MYSQL_DATABASE

    # Engines, on SQLAlchemy, are used to manage two crucial factors: Pools and Dialects
    self.engine = create_engine('mysql://%s:%s@localhost:%s/%s' % (self.username, self.password, str(self.port), self.db_name))

    # Call the session which bind the db engine to manipulate the database
    Session = sessionmaker(bind=self.engine)
    self.session = Session()

    # Make sure all tables exist
    self.create_tables_if_not_exist()

  def create_tables_if_not_exist(self):
    table_name = "Sensors"
    if not self.engine.dialect.has_table(self.engine, table_name):
      metadata = MetaData(self.engine)
      Table(table_name, metadata, Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True), 
            Column('Timestamp', DateTime, nullable=False),
            Column('Vivarium_id', Integer),
            Column('What', Text),
            Column('Location', Text),
            Column('Value', Float))
      metadata.create_all()

    table_name = "Vivarium"
    if not self.engine.dialect.has_table(self.engine, table_name):
      metadata = MetaData(self.engine)
      Table(table_name, metadata,
            Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Name', Text),
            Column('Height', Float),
            Column('Width', Float),
            Column('Depth', Float),
            Column('Picture', Text))
      metadata.create_all()

    table_name = "Animal"
    if not self.engine.dialect.has_table(self.engine, table_name):
      metadata = MetaData(self.engine)
      Table(table_name, metadata,
            Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Name', Text),
            Column('Vivarium_id', Integer),
            Column('Species', Text),
            Column('Morph', Text),
            Column('Dob', Text),
            Column('Picture', Text))
      metadata.create_all()

    table_name = "Physics"  # Length and Weight
    if not self.engine.dialect.has_table(self.engine, table_name):
      metadata = MetaData(self.engine)
      Table(table_name, metadata, Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Animal_id', Integer),
            Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now),
            Column('What', Text),
            Column('Value', Float))
      metadata.create_all()

    table_name = "Feedings"
    if not self.engine.dialect.has_table(self.engine, table_name):
      metadata = MetaData(self.engine)
      Table(table_name, metadata,
            Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Animal_id', Integer),
            Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now),
            Column('What', Text),
            Column('Prekilled', Boolean),
            Column('Refused', Boolean))
      metadata.create_all()

    table_name = "Notes"
    if not self.engine.dialect.has_table(self.engine, table_name):
      metadata = MetaData(self.engine)
      Table(table_name, metadata,
            Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Animal_id', Integer),
            Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now),
            Column('Note', Text))
      metadata.create_all()

    table_name = "Sheddings"
    if not self.engine.dialect.has_table(self.engine, table_name):
      metadata = MetaData(self.engine)
      Table(table_name, metadata,
            Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Animal_id', Integer),
            Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now),
            Column('Successful', Boolean),
            Column('Note', Text))
      metadata.create_all()

  # QUERY METHODS:
  # count(): Returns the total number of rows of a query.
  # filter(): Filters the query by applying a criteria. http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.filter
  # delete(): Removes from the database the rows matched by a query.
  # distinct(): Applies a distinct statement to a query.
  # exists(): Adds an exists operator to a subquery.
  # first(): Returns the first row in a query.
  # get(): Returns the row referenced by the primary key parameter passed as argument.
  # join(): Creates a SQL join in a query.
  # limit(): Limits the number of rows returned by a query.
  # order_by(): Sets an order in the rows returned by a query.

  # Usage: add_entry(Tables.Sensors(vivarium_id=1, what="Temperature", location="Hot side", value=0.0))
  def add_record(self, record):
    self.session.add(record)
    self.session.commit()

  def add_records(self, records):
    self.session.add_all(records)
    self.session.commit()

  def save(self):
    self.session.commit()

  # Usage: get_all_records(Tables.Sensors)
  def get_all_records(self, table):
    return self.session.query(table).all()

  # Usage: query(Table.Sensors, what="Temperature")
  def query(self, table, **kwargs):
    return self.session.query(table).filter_by(**kwargs).first()

  def query_all(self, table, **kwargs):
    return self.session.query(table).filter_by(**kwargs).all()

  def delete_records(self, table, **kwargs):
    records_to_delete = self.session.query(table).filter_by(**kwargs).all()
    for record in records_to_delete:
      self.session.delete(record)
    self.session.commit()

  # ToDo: https://stackoverflow.com/questions/17868743/doing-datetime-comparisons-in-filter-sqlalchemy


Base = declarative_base()
class Tables:

  # Deprecated
  def get(self, arg):
    try:
        return eval("self.%s" % arg)
    except:
      return None

class Sensors(Tables, Base):
  __tablename__ = 'Sensors'

  id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
  timestamp = Column('Timestamp', DateTime, nullable=False)
  vivarium_id = Column('Vivarium_id', Integer)
  what = Column('What', Text)
  location =  Column('Location', Text)
  value = Column('Value', Float)

  def __init__(self, timestamp=datetime.now(), vivarium_id=None, what=None, location=None, value=None):
    self.timestamp = timestamp
    self.vivarium_id = vivarium_id
    self.what = what
    self.location = location
    self.value = value


class Vivarium(Tables, Base):
  __tablename__ = 'Vivarium'

  id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
  name = Column('Name', Text)
  height = Column('Height', Float)
  width = Column('Width', Float)
  depth =  Column('Depth', Float)
  picture = Column('Picture', Text)

  def __init__(self, name=None, height=None, width=None, depth=None, picture=None):
    self.name = name
    self.height = height
    self.width = width
    self.depth = depth
    self.picture = picture


class Animal(Tables, Base):
  __tablename__ = 'Animal'

  id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
  name = Column('Name', Text)
  vivarium_id = Column('Vivarium_id', Integer)
  species = Column('Species', Text)
  morph =  Column('Morph', Text)
  dob = Column('Dob', Text)
  picture = Column('Picture', Text)

  def __init__(self, name="", vivarium_id=None, species=None, morph=None, dob=None, picture=None):
    self.name = name
    self.vivarium_id = vivarium_id
    self.species = species
    self.morph = morph
    self.dob = dob
    self.picture = picture


class Physics(Tables, Base):
  __tablename__ = 'Physics'

  id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
  timestamp = Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now)
  animal_id = Column('Animal_id', Integer)
  what = Column('What', Text)
  value = Column('Value', Float)

  def __init__(self, animal_id=None, what=None, value=None):
    self.animal_id = animal_id
    self.what = what
    self.value = value


class Feedings(Tables, Base):
  __tablename__ = 'Feedings'

  id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
  timestamp = Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now)
  animal_id = Column('Animal_id', Integer)
  what = Column('What', Text)
  prekilled = Column('Prekilled', Boolean)
  refused = Column('Refused', Boolean)

  def __init__(self, animal_id=None, what=None, prekilled=None, refused=None):
    self.animal_id = animal_id
    self.what = what
    self.prekilled = prekilled
    self.refused = refused


class Notes(Tables, Base):
  __tablename__ = 'Notes'

  id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
  timestamp = Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now)
  animal_id = Column('Animal_id', Integer)
  note = Column('Note', Text)

  def __init__(self, animal_id=None, note=None):
    self.animal_id = animal_id
    self.note = note


class Sheddings(Tables, Base):
  __tablename__ = 'Sheddings'

  id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
  timestamp = Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now)
  animal_id = Column('Animal_id', Integer)
  successful = Column('Successful', Boolean)
  note = Column('Note', Text)

  def __init__(self, animal_id=None, successful=None, note=None):
    self.animal_id = animal_id
    self.successful = successful
    self.note = note