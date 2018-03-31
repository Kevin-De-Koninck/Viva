from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
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

    import ipdb; ipdb.set_trace()

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
            Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now), Column('Vivarium_id', Integer),
            Column('What', String(100)),
            Column('Location', String(100)),
            Column('Value', Float))
      metadata.create_all()

    table_name = "Vivarium"
    if not self.engine.dialect.has_table(self.engine, table_name):
      metadata = MetaData(self.engine)
      Table(table_name, metadata,
            Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Name', String(100)),
            Column('Height', Float),
            Column('Width', Float),
            Column('Depth', Float),
            Column('Picture', String(100)))
      metadata.create_all()

    table_name = "Animal"
    if not self.engine.dialect.has_table(self.engine, table_name):
      metadata = MetaData(self.engine)
      Table(table_name, metadata,
            Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Name', String(100)),
            Column('Vivarium_id', Integer),
            Column('Species', String(100)),
            Column('Morph', String(100)),
            Column('Dob', String(100)),
            Column('Picture', String(100)))
      metadata.create_all()

    table_name = "Physics"  # Length and Weight
    if not self.engine.dialect.has_table(self.engine, table_name):
      metadata = MetaData(self.engine)
      Table(table_name, metadata, Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Animal_id', Integer),
            Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now),
            Column('What', String(100)),
            Column('Value', Float))
      metadata.create_all()

    table_name = "Feedings"
    if not self.engine.dialect.has_table(self.engine, table_name):
      metadata = MetaData(self.engine)
      Table(table_name, metadata,
            Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Animal_id', Integer),
            Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now),
            Column('What', String(100)),
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
            Column('Note', String(1000)))
      metadata.create_all()

    table_name = "Sheddings"
    if not self.engine.dialect.has_table(self.engine, table_name):
      metadata = MetaData(self.engine)
      Table(table_name, metadata,
            Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True),
            Column('Animal_id', Integer),
            Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now),
            Column('Successful', Boolean),
            Column('Note', String(1000)))
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

  # Usage: get_all_records(Tables.Sensors)
  def get_all_records(self, table):
    return self.session.query(table).all()

  # Usage: query(Table.Sensors, what="Temperature")
  def query(self, table, **kwargs):
    return self.session.query(table).filter_by(**kwargs)

  def delete_records(self, table, **kwargs):
    records_to_delete = self.session.query(table).filter_by(**kwargs)
    for record in records_to_delete:
      self.session.delete(record)
    self.session.commit()

  # ToDo: https://stackoverflow.com/questions/17868743/doing-datetime-comparisons-in-filter-sqlalchemy



class Tables:
  Base = declarative_base()


  class Sensors(Base):
    __tablename__ = 'Sensors'

    id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
    timestamp = Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now)
    vivarium_id = Column('Vivarium_id', Integer)
    what = Column('What', String(100))
    location =  Column('Location', String(100))
    value = Column('Value', Float)

    def __init__(self, vivarium_id=1, what="Temperature", location="Hot side", value=0.0):
      self.vivarium_id = vivarium_id
      self.what = what
      self.location = location
      self.value = value


  class Vivarium(Base):
    __tablename__ = 'Vivarium'

    id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column('Name', String(100))
    height = Column('Height', Float)
    width = Column('Width', Float)
    depth =  Column('Depth', Float)
    picture = Column('Picture', String(100))

    def __init__(self, name="default", height=0.0, width=0.0, depth=0.0, picture=None):
      self.name = name
      self.height = height
      self.width = width
      self.depth = depth
      self.picture = picture


  class Animal(Base):
    __tablename__ = 'Animal'

    id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column('Name', String(100))
    vivarium_id = Column('Vivarium_id', Integer)
    species = Column('Species', String(100))
    morph =  Column('Morph', String(100))
    dob = Column('Dob', String(100))
    picture = Column('Picture', String(100))

    def __init__(self, name="default_name", vivarium_id=1, species="default", morph="default", dob="2018/02/24", picture=None):
      self.name = name
      self.vivarium_id = vivarium_id
      self.species = species
      self.morph = morph
      self.dob = dob
      self.picture = picture


  class Physics(Base):
    __tablename__ = 'Physics'

    id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
    timestamp = Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now)
    animal_id = Column('Animal_id', Integer)
    what = Column('What', String(100))
    value = Column('Value', Float)

    def __init__(self, animal_id=1, what="Length", value=0.0):
      self.animal_id = animal_id
      self.what = what
      self.value = value


  class Feedings(Base):
    __tablename__ = 'Feedings'

    id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
    timestamp = Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now)
    animal_id = Column('Animal_id', Integer)
    what = Column('What', String(100))
    prekilled = Column('Prekilled', Boolean)
    refused = Column('Refused', Boolean)

    def __init__(self, animal_id=1, what="Adult rat", prekilled=True, refused=False):
      self.animal_id = animal_id
      self.what = what
      self.prekilled = prekilled
      self.refused = refused


  class Notes(Base):
    __tablename__ = 'Notes'

    id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
    timestamp = Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now)
    animal_id = Column('Animal_id', Integer)
    note = Column('Note', String(1000))

    def __init__(self, animal_id=1, note="default"):
      self.animal_id = animal_id
      self.note = note


  class Sheddings(Base):
    __tablename__ = 'Sheddings'

    id = Column('Id', Integer, primary_key=True, nullable=False, autoincrement=True)
    timestamp = Column('Timestamp', DateTime, nullable=False, onupdate=datetime.now)
    animal_id = Column('Animal_id', Integer)
    successful = Column('Successful', Boolean)
    note = Column('Note', String(1000))

    def __init__(self, animal_id=1, successful=True, note=""):
      self.animal_id = animal_id
      self.successful = successful
      self.note = note