from persistent import Persistent

class PersistantIndexer(Persistent):
  # prepend _v_ to make it volatilive
  _v_book = None
  def __init__(self):
    self._v_book = Book()
    self._v_book.addData(self)
  def __setattr__(self, name, value):
    #only run this if the name is within the current objects attributes
    if self._v_book and name not in Persistent.__dict__:
      # if the book exists AND
      # if the value has changed
      # and that attribute is an indexable attribute
      # OR we want it to be indexed, however it is not actually in the index (this condition will be caught 
      # in updateIndexedValue)
      if self._v_book and self.__dict__.get(name) != value and name in self.indexable:
        self._v_book.updateIndexedValue(self, name, value)
      # save changes
      self._v_book.commitTransaction()
    Persistent.__setattr__(self, name, value)


  #TODO
  def __delattr__(self, name):
    pass
