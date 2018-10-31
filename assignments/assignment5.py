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

   username     = Column(String(20), unique = True, primary_key = True)
   first        = Column(String(40), )
   last         = Column(String(40), )
   affiliation  = Column(String(40), default = 'None')

   events_owned = relationship("Event", back_populates = "owner")
   invites      = relationship("Invite", back_populates = "user")

   def __repr__(self):
      return "User<{0} {1} {2}>".format(self.username, self.first, self.last)

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

   owner      = relationship("User", back_populates = "events_owned")
   invites    = relationship("Invite", back_populates = "event")

   def __repr__(self):
      return "Event<{0}>".format(self.title)

# Create our Invite class
class Invite(Base):
   __tablename__ = 'ev_invites'

   event_id = Column(Integer, ForeignKey('ev_events.id'), primary_key = True, nullable = False)
   username = Column(String(20), ForeignKey('ev_users.username'), nullable = False)
   status   = Column(Enum(Status), primary_key = True, nullable = True)

   user     = relationship("User", back_populates = "invites")
   event    = relationship("Event", back_populates = "invites")

   def __repr__(self):
      return "Invite<{0} {1}>".format(self.username, self.status)

###### END OF CLASS AND TABLE DEFINITIONS

# Drop existing tables and recreate them
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

###### WRITE YOUR ANSWERS TO OTHER QUESTIONS HERE

# Number 6 - Create User object for myself and one professor, add to session, then commit
userPatrick = User(username="conboyp", first="Patrick", last="Conboy", affiliation="Hanover College, Student")
userHaris   = User(username="skiadash", first="Haris", last="Skiadas", affiliation="Hanover College, Faculty, Staff")
session.add(userPatrick)
session.add(userHaris)
session.commit()


# Number 7 - Add 100 student User objects, add to session, then commit
studentUserList = [User(username="student{0}".format(x), first="Number{0}".format(x), last="Student", affiliation="Hanover College, Student") for x in range(1, 101)]
##### .format is apparently being used to phase out the % formatting method. That's why I opted to use that here instead.
session.add_all(studentUserList)
session.commit()


# Number 8 - create a 'Homecoming get-together' Event object, add to session, then commit
homecomingEvent = Event(title="Homecoming get-together" , longitude=38.71 , latitude=85.46 , owner_name="conboyp" , start=datetime(2018, 10, 6, 8, 0, 0))
session.add(homecomingEvent)
session.commit()


# Number 9 - create 100 Invite objects to the 'Homecoming get-together' Event for all 100 students added before
homecomingInvites = [Invite(event=homecomingEvent , user=student) for student in studentUserList]
session.add_all(homecomingInvites)
session.commit()

###### BELOW THIS LINE YOU CAN ADD ANY CODE YOU WANT TO HAVE FOR TESTING

