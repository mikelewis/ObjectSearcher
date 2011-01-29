from book import Book
from indexable import Indexable
import unittest

class Person(Indexable):
  name = None
  age = None
  indexableAttrs = ('name', )

class Animal(Indexable):
  kind = None
  color = None
  indexableAttrs = ('kind', )
  def __init__(self, kind="", color=""):
    Indexable.__init__(self)
    self.kind = kind
    self.color = color

class TestOjectSearcher(unittest.TestCase):
  def setUp(self):
    self.book = Book()
    self.person = Person()
    self.person.name = "Mike"
    self.person.age = 20
    person1 = Person()
    person1.name = "Jouhan"
    person1.age = 22
    person2 = Person()
    person2.age = "Alex"
    person2.age = 20
    horse = Animal("Horse", "Brown")
    fox = Animal("Fox", "Red")

  def test_index_has_classes(self):
    klasses = ('Person', )
    for klass in klasses:
      self.assertTrue(klass in self.book.indexdb)

  def test_index_has_classes_built_with_constructor(self):
    klasses = ('Animal', )
    for klass in klasses:
      self.assertTrue(klass in self.book.indexdb)

  def test_index_has_indexed_person_attributes(self):
    self.assertTrue("name" in self.book.indexdb["Person"])

  def test_index_has_declared_values_for_person(self):
    self.assertEqual(['Jouhan', 'Mike'], list(self.book.indexdb['Person']['name'].keys()))

  def test_index_has_declared_objects_for_person(self):
    self.assertEqual(id(self.person), id(self.book.indexdb['Person']['name'].values('Mi')[0]))



if __name__ == '__main__':
  unittest.main()  
