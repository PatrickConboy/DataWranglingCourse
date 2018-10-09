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

# Adding our tables (problem 1)
tblUsers = Table('ev_users', metadata,
  Column('username', String(20), unique = True, primary_key = True),
  Column('first', String(40)),
  Column('last', String(40)),
  Column('affiliation', String(40), default = 'None')
)

# Drop existing tables
metadata.drop_all(engine)
# Create these tables if they do not exist
metadata.create_all(engine)

conn = engine.connect()

print(tblUsers);