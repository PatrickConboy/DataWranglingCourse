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

###### END OF CLASS AND TABLE DEFINITIONS

# Drop existing tables and recreate them
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

###### WRITE YOUR ANSWERS TO OTHER QUESTIONS HERE





###### BELOW THIS LINE YOU CAN ADD ANY CODE YOU WANT TO HAVE FOR TESTING

