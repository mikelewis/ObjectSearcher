from persistent import Persistent
from BTrees.OOBTree import OOBTree
from ZODB import FileStorage, DB
import transaction

class Book(object):
  storage = None
  db = None
  dbroot = None
  conn = None
  indexdb = None
  __shared_state = {}
  def __init__(self):
    self.__dict__ = self.__shared_state
    self.storage = self.storage or FileStorage.FileStorage('indexes.db')
    self.db = self.db or DB(self.storage)
    self.conn = self.conn or self.db.open()
    self.dbroot = self.dbroot or self.conn.root()

    if not self.dbroot.has_key('indexdb'):
      self.dbroot['indexdb'] = OOBTree()
    if not self.indexdb:
      self.indexdb = self.dbroot['indexdb']
  
  def __del__(self):
    self.db.close()

  def addData(self, data):
    klassName = self.getClassName(data) 
    if klassName not in self.indexdb:
      self.indexdb[klassName] = OOBTree()

  def updateIndexedValue(self, obj, attrName, newAttrValue):
    klassName = self.getClassName(obj)
    # gets that classes index tree
    klassIndex = self.indexdb.get(klassName)
    oldValue = obj.__dict__.get(attrName)
    if attrName in klassIndex and oldValue in klassIndex[attrName]:
      del klassIndex[attrName][oldValue]
    #this will run no matter if the attribute exist or not
    self.setIndexValue(obj, attrName, newAttrValue)

  def setIndexValue(self, obj, name, value):
    klassName = self.getClassName(obj)
    self.indexdb.get(klassName).setdefault(name, OOBTree())[value] = obj

  #TODO
  def removeIndexedValue(self, obj, name, value):
    klassName = self.getClassName(obj)
    if self.index.get(klassName).get(name, None) and self.indexdb.get(klassName).get(name).get(value, None):
      del self.index.get(klassName)[name][value]

  def getClassName(self, obj):
    return obj.__class__.__name__

  def commitTransaction(self):
    transaction.commit()
