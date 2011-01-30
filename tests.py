from book import Book
from indexable import Indexable
from persistent.mapping import PersistentMapping
import unittest
import os
from searcher import Searcher


# Set database name to test
os.environ['object_searcher_database'] = "tests.db"

class Person(Indexable):
  name = None
  age = None
  indexableAttrs = ('name', 'age', )
  def __init__(self, name=None, age=None):
    Indexable.__init__(self)
    self.name = name
    self.age = age

class Animal(Indexable):
  kind = None
  color = None
  indexableAttrs = ('kind', )
  def __init__(self, kind="", color=""):
    Indexable.__init__(self)
    self.kind = kind
    self.color = color

class TestSearcher(unittest.TestCase):

  def setUp(self):
    self.searcher = Searcher()
    self.mikeObj = Person("mike", 15)
    self.mikeObj2 = Person("mike", 99)
    self.jouhan = Person("Jouhan", 22)
    self.jouhan1 = Person("Jouhan", 74)
    self.alex = Person("Alex", 15)

  def tearDown(self):
    #to destroy the database that was created for testing AKA ISOLATION!
    self.searcher.index.clear()

  def test_searcher_expecting_multiple_values(self):
    self.assertEquals(len(self.searcher.fromClass("Person").where("age = 15")), 2)

  def test_searcher_excepting_no_values(self):
    self.assertEquals(len(self.searcher.fromClass('Person').where("age = 20")), 0)

  def test_searcher_excepting_correct_result(self):
    person = self.searcher.fromClass("Person").where("age = 99")[0]
    self.assertTrue(self.mikeObj2.__hash__() == person.__hash__())

  def test_searcher_excepting_one_result(self):
    people = self.searcher.fromClass("Person").where("age = 99")
    self.assertTrue(len(people) == 1)

  def test_searcher_equality_search(self):
    person = self.searcher.fromClass("Person").where("name = Alex")[0]
    self.assertTrue(person.__hash__(), self.alex.__hash__())

  def test_searcher_greater_or_equal_to_search_two_results(self):
    people = self.searcher.fromClass("Person").where("age >= 74")
    self.assertTrue(len(people), 2)

  def test_searcher_greater_or_equal_to_search_correct_results(self):
    people = self.searcher.fromClass("Person").where("age >= 74")
    hashes = [person.__hash__() for person in people]
    self.assertTrue(self.mikeObj2.__hash__() in hashes)

  def test_searcher_greater_search_two_results(self):
    people = self.searcher.fromClass("Person").where("age > 74")
    self.assertTrue(len(people), 1)

  def test_searcher_greater_to_search_correct_results(self):
    people = self.searcher.fromClass("Person").where("age > 74")
    hashes = [person.__hash__() for person in people]
    self.assertTrue(self.mikeObj2.__hash__() in hashes)

  def test_searcher_between_search_four_results(self):
    people = self.searcher.fromClass("Person").where("age BETWEEN 15 AND 74")
    self.assertTrue(len(people), 4)

  def test_searcher_between_search_correct_results(self):
    people = self.searcher.fromClass("Person").where("age BETWEEN 15 AND 74")
    hashes = [person.__hash__() for person in people]
    self.assertTrue(self.mikeObj.__hash__() in hashes and self.jouhan.__hash__() in hashes and self.alex.__hash__() in hashes and self.jouhan1.__hash__() in hashes)


    




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

  def tearDown(self):
    #to destroy the database that was created for testing AKA ISOLATION!
    self.book.indexdb.clear()

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
    # its complaing because Tim is in the database (look at 63)
    self.assertEqual(['Jouhan', "Mike"], list(self.book.indexdb['Person']['name'].keys()))

  def test_index_has_declared_objects_for_person(self):
    self.assertEqual(self.person.__hash__(), self.book.indexdb['Person']['name']['Mike'].values()[0].__hash__())

  def test_index_can_track_changed_ojects(self):
    mike = self.book.indexdb['Person']['name']['Mike'].values()[0]
    oldAge = mike.age
    #change age
    mike.age = 25
    self.assertEqual(self.book.indexdb['Person']['name']['Mike'].values()[0].age, 25)

  def test_index_update_indexableAttributes(self):
    mike = self.book.indexdb['Person']['name']['Mike'].values()[0]
    mike.name = "Tim"
    self.assertTrue("Tim" in self.book.indexdb['Person']['name'].keys())
    self.assertTrue("Mike" not in self.book.indexdb['Person']['name'].keys())

  def test_update_index_with_none_value(self):
    mike = self.book.indexdb['Person']['name']['Mike'].values()[0]
    mike.name = None
    self.assertTrue(None not in self.book.indexdb['Person']['name'])
    self.assertTrue("Mike" not in self.book.indexdb['Person']['name'])

  def test_index_supports_multiple_values_per_key(self):
    mikePerson = Person()
    mikePerson.name = "Mike" #aka DUPLICATE VALUE FOR THAT ATTR
    mikePerson.age = 99
    self.assertTrue(len(self.book.indexdb['Person']['name']['Mike'].values()) == 2)



if __name__ == '__main__':
  unittest.main()  
