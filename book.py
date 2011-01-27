from persistent import Persistent
from BTrees.OOBTree import OOBTree
from ZODB import FileStorage, DB
import transaction

class Book(Persistent):
  indexedClasses = set()
  storage = None
  db = None
  dbroot = None
  conn = None
  indexdb = None
  def __init__(self):
    self.storage = FileStorage.FileStorage('indexes.db')
    self.db = DB(self.storage)
    self.conn = self.db.open()
    self.dbroot = self.conn.root()

    if not self.dbroot.has_key('indexdb'):
      self.dbroot['indexdb'] = OOBTree()
    self.indexdb = self.dbroot['indexdb']

  def addData(self, data):
    klassName = data.__class__.__name__
    self.indexedClasses.add(klassName)
    for indexable in data.indexable:
      self.indexdb.setdefault(klassName, OOBTree())[getattr(data, indexable)] = data
    transaction.commit()
