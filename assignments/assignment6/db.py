# Sets up database
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from json import dumps

Base = declarative_base()

# Bucket class defines an object with an id that has a shortcut assigned to it
class Bucket(Base):
   __tablename__ = 'buckets'

   id           = Column(String(40), nullable = False, primary_key = True)
   description  = Column(String(200))
   passwordHash = Column(String(40), nullable = False)

   shortcuts    = relationship("Shortcut", back_populates = "bucket")

   def __repr__(self):
      return "Bucket <{0} {1}>".format(self.id, self.description)

# Shortcut class defines an object that contains the bucketId, original link, and possible description
class Shortcut(Base):
   __tablename__ = 'shortcuts'

   linkHash    = Column(String(40), nullable = False, primary_key = True)
   bucketId    = Column(String(40), ForeignKey('buckets.id', ondelete="CASCADE"), nullable = False, primary_key = True)
   link        = Column(String(200), nullable = False)
   description = Column(String(200))

   bucket      = relationship("Bucket", back_populates = "shortcuts")

   def __repr__(self):
      return "Shortcut <{0} {1}>".format(self.linkHash, self.description)

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
      return self.session.query(Bucket).all()

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