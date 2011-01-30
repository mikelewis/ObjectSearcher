from persistent.mapping import PersistentMapping
from BTrees.OOBTree import OOBTree
from ZODB import FileStorage, DB
import transaction
import os

class Book(object):
  storage = None
  db = None
  dbroot = None
  conn = None
  indexdb = None
  database_name = None
  num_book_instances = {"count":0}
  __shared_state = {}
  def __init__(self):
    self.__dict__ = self.__shared_state
    self.num_book_instances['count'] += 1
    self._rebuild_db()


  def _rebuild_db(self):
    self.database_name = os.environ.get("object_searcher_database", "indexes.db")
    self.storage = self.storage or FileStorage.FileStorage(self.database_name)
    self.db = self.db or DB(self.storage)
    self.conn = self.conn or self.db.open()
    self.dbroot = self.dbroot or self.conn.root()
    if not self.dbroot.has_key('indexdb'):
      self.dbroot['indexdb'] = OOBTree()
    if not self.indexdb:
      self.indexdb = self.dbroot['indexdb']


  def __del__(self):
    pass
  # self.db.close()

  def addData(self, data):
    klassName = self.getClassName(data) 
    if klassName not in self.indexdb:
      self.indexdb[klassName] = OOBTree()

  def updateIndexedValue(self, obj, attrName, newAttrValue):
    klassName = self.getClassName(obj)
    # gets that classes index tree
    klassIndex = self.indexdb.get(klassName)
    oldValue = obj.__dict__.get(attrName)
    if newAttrValue is not None:
      if attrName in klassIndex and oldValue != newAttrValue and oldValue in klassIndex[attrName]:
        del klassIndex[attrName][oldValue][obj.__hash__()]
      #this will run no matter if the attribute exist or not
      self.setIndexValue(obj, attrName, newAttrValue)
    else:
      if oldValue in klassIndex[attrName]:
        del klassIndex[attrName][oldValue]

  def setIndexValue(self, obj, name, value):
    klassName = self.getClassName(obj)
    self.indexdb.get(klassName).setdefault(name, OOBTree()).setdefault(value, PersistentMapping())[obj.__hash__()]= obj

  #TODO
  def removeIndexedValue(self, obj, name, value):
    klassName = self.getClassName(obj)
    if self.index.get(klassName).get(name, None) and self.indexdb.get(klassName).get(name).get(value, None):
      del self.index.get(klassName)[name][value]

  def getClassName(self, obj):
    return obj.__class__.__name__

  def commitTransaction(self):
    transaction.commit()
