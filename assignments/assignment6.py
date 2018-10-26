# Name:

import random
from datetime import datetime, timedelta
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# The Status class is used in the enum column that you create in question 3
# enum package documentation: https://docs.python.org/3/library/enum.html
import enum
class Status(enum.Enum):
    Accepted = 1
    Declined = 2
    Maybe = 3

engine = create_engine('sqlite:///:memory:', echo=True)

# Create our User class
class User(Base):
   __tablename__ = 'ev_users'

   username    = Column(String(20), unique = True, primary_key = True)
   first       = Column(String(40), )
   last        = Column(String(40), )
   affiliation = Column(String(40), default = 'None')

   def __repr__(self):
      return "User<%s %s>" % (self.first, self.last)

# Create our Event class
class Event(Base):
   __tablename__ = 'ev_events'

   id         = Column(Integer, unique = True, nullable = False, primary_key = True, autoincrement = True)
   title      = Column(String(40), nullable = False, default = "")
   longitude  = Column(Float(precision = 32))
   latitude   = Column(Float(precision = 32))
   owner_name = Column(String(20), ForeignKey('ev_users.username'), nullable = False)
   start      = Column(DateTime, default = datetime.now())
   end        = Column(DateTime, default = None)

   def __repr__(self):
      return "Event<%s>" % (self.title)

###### END OF CLASS AND TABLE DEFINITIONS

# Drop existing tables and recreate them
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

###### WRITE YOUR ANSWERS TO OTHER QUESTIONS HERE





###### BELOW THIS LINE YOU CAN ADD ANY CODE YOU WANT TO HAVE FOR TESTING

