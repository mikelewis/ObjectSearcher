from book import Book
from indexable import Indexable

# Test Class... nothing else
class Person(Indexable):
  name = None
  age = None
  indexableAttrs = ('name','age', )

if __name__ == '__main__':
  #p = Person()
  #p.name = "Mike"
  #p.age = 22
  #p1 = Person()
  #p1.name = "Matt"
  #p1.age = 30
  #p2 = Person()
  #p2.name = "Mitch"
  #p2.age = 25
  #p3 = Person()
  #p3.name = "Bob"
  #p3.age = 21
  #p4 = Person()
  #p4.name = "Tim"
  #p4.age = 25
  
  book1 = Book()
  print list(book1.indexdb['Person']['name'].keys())
  print list(book1.indexdb['Person']['age'].keys())
