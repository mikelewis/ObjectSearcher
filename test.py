from book import Book
from persistent import Persistent

# Test Class... nothing else
class Person(Persistent):
  name = None
  age = None
  indexable = ('name',)

if __name__ == '__main__':
  book = Book()
  p = Person()
  p.name = "Mike"
  age = 20
  p1 = Person()
  p1.name = "Matt"
  p1.age = 30
  p2 = Person()
  p2.name = "Mitch"
  p2.age = 25
  p3 = Person()
  p3.name = "Bob"
  p3.age = 21
  book.addData(p)
  book.addData(p1)
  book.addData(p2)
  book.addData(p3)
  """
  #2nd run
  p2 = book.indexdb['Person']['Mitch']
  p2.name = "Mitch1aasdf"
  p2.age = 25
  """
  print map(lambda x: x.name, book.indexdb['Person'].values("Mi"))
