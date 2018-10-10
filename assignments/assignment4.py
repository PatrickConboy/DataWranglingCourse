# Name:
## Reading database keys
import json
with open('keys.json', 'r') as f:
   account_info = json.loads(f.read())
   vault = account_info['vault']

from datetime import datetime, timedelta
from sqlalchemy import *

# The Status class is used in the enum column that you create in question 3
# enum package documentation: https://docs.python.org/3/library/enum.html
import enum
class Status(enum.Enum):
    Accepted = 1
    Declined = 2
    Maybe = 3

engineString = 'mysql+mysqldb://{username}:{password}@{server}/{schema}'
engineUrl = engineString.format(**vault)

# Establishing a specific database connection
engine = create_engine('sqlite:///:memory:', echo=True)

metadata = MetaData()

# Adding our tables
# Problem 1
tblUsers = Table('ev_users', metadata,
  Column('username', String(20), unique = True, primary_key = True),
  Column('first', String(40)),
  Column('last', String(40)),
  Column('affiliation', String(40), default = 'None')
)

# Problem 2
tblEvents = Table('ev_events', metadata,
  Column('id', Integer, unique = True, nullable = False, primary_key = True, autoincrement = True),
  Column('title', String(40), nullable = False, default = ""),
  Column('longitude', Float(precision=32)),
  Column('latitude', Float(precision=32)),
  Column('owner', String(20),
    ForeignKey("ev_users.username"),
    nullable = False),
  Column('start', DateTime, default = datetime.now()),
  Column('end', DateTime, default = null)
)

# Problem 3
tblInvites = Table('ev_invites', metadata,
  Column('event_id', Integer,
    ForeignKey("ev_events.id", ondelete="CASCADE"),
    nullable = False),
  Column('username', String(20),
    ForeignKey("ev_users.username", ondelete="CASCADE"),
    nullable = False),
  Column('status', Enum(Status), nullable = True)
)

# Drop existing tables
metadata.drop_all(engine)
# Create these tables if they do not exist
metadata.create_all(engine)

conn = engine.connect()

# Problem 4
users = [
  { "username": "conboyp", "first": "patrick", "last": "conboy", "affiliation": "Hanover College, Student" },
  { "username": "jarnagink", "first": "kenny", "last": "jarnagin", "affiliation": "Hanover College, Student" },
  { "username": "skiadasc", "first": "charilaos", "last": "skiadas", "affiliation": "Hanover College, Faculty, Staff" }
]
ins = tblUsers.insert()  # Create our insert object
result = conn.execute(ins, users)  # Execute the insert on a connection

# Problem 5
event = [
  {"title": "Homecoming get-together", "longitude": 38.71, "latitude": 85.46, "owner": "conboyp", "start": 'October 6th @ 8 AM' }
]
ins = tblEvents.insert()  # Create our insert object
result = conn.execute(ins, event)  # Execute the insert on a connection