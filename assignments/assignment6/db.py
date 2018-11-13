# Sets up database
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from json import dumps

Base = declarative_base()

class Bucket(Base):
   __tablename__ = 'buckets'
   # TODO Will need to add the fields for the Bucket class here

   def __repr__(self):
      return "TODO: You must implement the __repr__ method in Bucket"


class Shortcut(Base):
   __tablename__ = 'shortcuts'
   # TODO Will need to add the fields for the Shortcut class here

   def __repr__(self):
      return "TODO: You must implement the __repr__ method in Shortcut"

# Represents the database and our interaction with it
class Db:
   def __init__(self):
      engineName = 'sqlite:///test.db'   # Uses in-memory database
      self.engine = create_engine(engineName)
      self.metadata = Base.metadata
      self.metadata.bind = self.engine
      self.metadata.drop_all(bind=self.engine)
      self.metadata.create_all(bind=self.engine)
      Session = sessionmaker(bind=self.engine)
      self.session = Session()

   def commit(self):
      self.session.commit()

   def rollback(self):
      self.session.rollback()

   # TODO Must implement the following methods
   def getBuckets(self):
      pass

   def getBucket(self, id):
      pass

   def addBucket(self, id, passwordHash, description=None):
      pass

   def deleteBucket(self, bucket):
      pass

   def getShortcut(self, linkHash, bucket):
      pass

   def addShortcut(self, linkHash, bucket, link, description=None):
      pass

   def deleteShortcut(self, shortcut):
      pass

   # TODO: May need to add your own db functions here