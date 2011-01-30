from persistent.mapping import PersistentMapping
from book import Book
from indexable import Indexable
import os

os.environ['object_searcher_database'] = "tests.db"

class IndexClassError(Exception):
  pass
class IndexAttributeError(Exception):
  pass
class ClassAttributeError(Exception):
  pass
class UnknownOperationError(Exception):
  pass
class IndexNoValuesError(Exception):
  pass

class Person(Indexable):
  name = None
  age = None
  indexableAttrs = ('name', 'age', )
  def __init__(self, name, age):
    Indexable.__init__(self)
    self.name = name
    self.age = age

class Searcher(object):
  fromKlass = None
  select_attrs = []
  index = None
  _book = Book()
  def __init__(self):
    self.index = self._book.indexdb

  def _isInt(self, n):
    try:
      int(n)
      return True
    except ValueError:
      return False

  def fromClass(self, klass):
    if klass not in self.index:
      raise IndexClassError()
    self.fromKlass = klass
    return self
  
  def select(self, query):
    query = query.strip()
    if query != "*":
      for attr in query.split(", "):
        attr = attr.strip()
        if not hasattr(eval(self.fromKlass), attr):
          raise ClassAttributeError()
        else:
          self.select_attrs.append(attr)
    return self
  def where(self, query):
    values = []
    splitQuery = query.split(" ")
    if len(splitQuery) == 3:
      attr, op, value = splitQuery
      value = int(value) if self._isInt(value) else value
      values = [value]
    elif len(splitQuery) == 5:
      attr, op, value1, _, value2 = splitQuery
      value1 = int(value1) if self._isInt(value1) else value1
      value2 = int(value2) if self._isInt(value2) else value2
      values = [value1, value2]


    return self._parseQuery(attr, op, values)

  def _parseQuery(self, attr, op, values):
    if attr not in self.index[self.fromKlass]:
      raise IndexAttributeError()
    if len(values) == 0:
      raise IndexNoValuesError()

    if len(values) == 1:
      value = values[0]

    if op == "=":
      if value not in self.index[self.fromKlass][attr]:
        return []
      else:
        return self.index[self.fromKlass][attr][value].values()
    elif op == ">=":
      return self._treeItemsToList(self.index[self.fromKlass][attr].values(value))
    elif op == ">":
      return self._treeItemsToList(self.index[self.fromKlass][attr].values(value, excludemin=True))
    elif op == "BETWEEN" and len(values) == 2:
      return self._treeItemsToList(self.index[self.fromKlass][attr].values(values[0],values[1]))
    else:
      raise UnknownOperationError()

  def _treeItemsToList(self, treeItems):
    retList = []
    for treeItem in treeItems:
      for resultItem in treeItem.values():
        retList.append(resultItem)
    return retList

