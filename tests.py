from book import Book
from indexable import Indexable
from persistent.mapping import PersistentMapping
import unittest
import os
from searcher import Searcher
# Set database name to test
os.environ['object_searcher_database'] = "tests.db"



class Person(Indexable):
  firstName = None
  name = None
  age = None
  indexableAttrs = ('name', 'age', 'firstName', )
  def __init__(self, name=None, age=None, firstName=None):
    Indexable.__init__(self)
    self.name = name
    self.age = age
    self.firstName = firstName

class Animal(Indexable):
  kind = None
  color = None
  mammal = False
  indexableAttrs = ('kind', 'mammal', )
  def __init__(self, kind="", color="", mammal=False):
    Indexable.__init__(self)
    self.kind = kind
    self.color = color
    self.mammal = mammal

class TestSearcher(unittest.TestCase):

  def setUp(self):
    self.searcher = Searcher()
    self.mikeObj = Person("Mike", 15)
    self.mikeObj2 = Person("Mike", 99)
    self.mikeObj3 = Person("Mike", 15, "Michael")
    self.jouhan = Person("Jouhan", 22)
    self.jouhan1 = Person("Jouhan", 74)
    self.alex = Person("Alex", 15)
    self.tim = Person("Tim", 100)
    self.cat = Animal("Cat", "Red", True)
    self.fish1 = Animal("Fish", "Blue", False)
    self.fish2 = Animal("Fish", "Red", False)
    self.dog = Animal("Dog", "Black", True)
    self.human = Animal("Human", "White", True)

  def tearDown(self):
    #to destroy the database that was created for testing AKA ISOLATION!
    self.searcher.index.clear()

  def test_searcher_expecting_multiple_values(self):
    self.assertEquals(len(self.searcher.fromClass("Person").where("age = 15")), 3)

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

  def test_searcher_with_select_two_dicts(self):
    people = self.searcher.fromClass("Person").select("name, age").where("name = Mike")
    self.assertTrue({"name" : "Mike", "age" : 15} in people and {"name" : "Mike", "age" : 99} in people)

  def test_searcher_with_select_and_queries(self):
    people = self.searcher.fromClass("Person").select("name, age").where("name = Mike AND age = 99")
    self.assertTrue({"name" : "Mike", "age" : 99} in people)

  def test_searcher_with_select_and_queries_count(self):
    people = self.searcher.fromClass("Person").select("name, age").where("name = Mike AND age = 99")
    self.assertEquals(len(people), 1)

  def test_searcher_with_select_or_queries(self):
    people = self.searcher.fromClass("Person").select("name, age").where("name = Alex OR name = Tim")
    self.assertTrue({"name" : "Alex", "age" : 15} in people and {"name" : "Tim", "age" : 100} in people)

  def test_searcher_with_select_or_queries_count(self):
    people = self.searcher.fromClass("Person").select("name, age").where("name = Alex OR name = Tim")
    self.assertEquals(len(people), 2)

  def test_searcher_with_select_between_queries(self):
    people = self.searcher.fromClass("Person").select("name").where("age BETWEEN 70 AND 100")
    selfAssertTrue({"name" : "Jouhan"} in people and {"name" : "Mike"} in people and {"name" : "Tim"} in people)

  def test_searcher_with_select_between_queries(self):
    people = self.searcher.fromClass("Person").select("name").where("age BETWEEN 70 AND 100")
    self.assertEquals(len(people), 3)

  def test_searcher_with_true_value_query(self):
    animals = self.searcher.fromClass("Animal").where("mammal == True")
    hashes = [animal.__hash__() for animal in animals]
    self.assertTrue(self.human.__hash__() in hashes and self.cat.__hash__() in hashes and self.dog.__hash__() in hashes)

  def test_searcher_with_true_value_count(self):
    animals = self.searcher.fromClass("Animal").where("mammal == True")
    self.assertEquals(len(animals), 3)
  
  def test_searcher_with_false_value_query(self):
    animals = self.searcher.fromClass("Animal").where("mammal == False")
    hashes = [animal.__hash__() for animal in animals]
    self.assertTrue(self.fish1.__hash__() in hashes and self.fish2.__hash__() in hashes)

  def test_searcher_with_false_value_count(self):
    animals = self.searcher.fromClass("Animal").where("mammal == False")
    self.assertEquals(len(animals), 2)

  def test_searcher_change_attributes(self):
    people = self.searcher.fromClass("Person").where("age = 15")
    self.assertTrue(len(people) == 3)
    self.alex.age = 16
    self.assertTrue(len(self.searcher.fromClass("Person").where("age = 15")) == 2)

  def test_searcher_or_query_count(self):
    people = self.searcher.fromClass("Person").where("name = Jouhan OR name = Mike")
    self.assertTrue(len(people) == 5)
  
  def test_searcher_or_query(self):
    people = self.searcher.fromClass("Person").where("name = Jouhan OR name = Mike")
    hashes = [person.__hash__() for person in people]
    self.assertTrue(self.mikeObj.__hash__() in hashes and self.mikeObj2.__hash__() and self.jouhan.__hash__() in hashes and self.jouhan1.__hash__() in hashes)
 
  def test_searcher_and_query_count(self):
    people = self.searcher.fromClass("Person").where("age = 15 AND name = Mike")
    self.assertTrue(len(people) == 2)

  def test_searcher_and_query(self):
    people = self.searcher.fromClass("Person").where("age = 15 AND name = Mike")
    hashes = [person.__hash__() for person in people]
    self.assertTrue(self.mikeObj.__hash__() in hashes and self.alex.__hash__() not in hashes)

  def test_searcher_multiple_ands_query(self):
    people = self.searcher.fromClass("Person").where("age = 15 AND name = Mike AND firstName = Michael")
    hashes = [person.__hash__() for person in people]
    self.assertTrue(self.mikeObj3.__hash__() in hashes)

  def test_searcher_multiple_ands_query_count(self):
    people = self.searcher.fromClass("Person").where("age = 15 AND name = Mike AND firstName = Michael")
    self.assertTrue(len(people) == 1)


  def test_searcher_multiple_or_query(self):
    people = self.searcher.fromClass("Person").where("age = 99 OR name = Jouhan OR name = Alex")
    hashes = [person.__hash__() for person in people]
    self.assertTrue(self.mikeObj2.__hash__() in hashes and self.jouhan.__hash__() in hashes and self.jouhan1.__hash__() in hashes and self.alex.__hash__() in hashes)

  def test_searcher_multiple_or_query_count(self):
    people = self.searcher.fromClass("Person").where("age = 99 OR name = Jouhan OR name = Alex")
    self.assertTrue(len(people) == 4)

  def test_searcher_all_query(self):
    people = self.searcher.fromClass("Person").all()
    hashes = [person.__hash__() for person in people]
    self.assertTrue(self.mikeObj2.__hash__() in hashes and self.jouhan.__hash__() in hashes and self.jouhan1.__hash__() in hashes and self.alex.__hash__() in hashes and self.mikeObj.__hash__() in hashes and self.mikeObj3.__hash__() in hashes and self.tim.__hash__() in hashes)

  def test_searcher_all_query_count(self):
    people = self.searcher.fromClass("Person").all()
    self.assertTrue(len(people) == 7)
  
  def test_searcher_with_not_equals_query(self):
    people = self.searcher.fromClass("Person").where("name != Mike")
    hashes = [person.__hash__() for person in people]
    self.assertTrue(self.alex.__hash__() in hashes and self.tim.__hash__() in hashes and self.jouhan.__hash__() in hashes and self.jouhan1.__hash__() in hashes)

  def test_searcher_with_not_equals_count(self):
    people = self.searcher.fromClass("Person").where("name != Mike")
    self.assertTrue(len(people), 4)

  def test_searcher_with_not_equals_and_other_ops_query(self):
    people = self.searcher.fromClass("Person").where("name != Mike AND age > 15")
    hashes = [person.__hash__() for person in people]
    self.assertTrue(self.tim.__hash__() in hashes and self.jouhan.__hash__() in hashes and self.jouhan1.__hash__() in hashes)

  def test_searcher_with_not_equals_and_other_ops_count(self):
    people = self.searcher.fromClass("Person").select('age').where("name != Mike AND age > 15")
    self.assertEquals(len(people), 3)

  def test_searcher_with_multiple_not_equals_query(self):
    people = self.searcher.fromClass("Person").where("name != Mike AND age != 15")
    hashes = [person.__hash__() for person in people]
    self.assertTrue(self.tim.__hash__() in hashes and self.jouhan.__hash__() in hashes and self.jouhan1.__hash__() in hashes)

  def test_searcher_with_multiple_not_equals_count(self):
    people = self.searcher.fromClass("Person").select('age').where("name != Mike AND age != 15")
    self.assertEquals(len(people), 3)

  def test_searcher_with_multiple_not_equals_select_query(self):
    people = self.searcher.fromClass("Person").select('age').where("name != Mike AND age != 15")
    self.assertTrue({"age" : 22} in people and {"age" : 74} in people and {"age" : 100} in people)

  def test_searcher_with_multiple_not_equals_select_count(self):
    people = self.searcher.fromClass("Person").select('age').where("name != Mike AND age != 15")
    self.assertEquals(len(people), 3)
  
  def test_searcher_with_not_equals_select_query(self):
    people = self.searcher.fromClass("Person").select('age').where("name != Mike")
    self.assertTrue({"age" : 22} in people and {"age" : 74} in people and {"age" : 15} in people and {"age" : 100} in people)

  def test_searcher_with_not_equals_select_count(self):
    people = self.searcher.fromClass("Person").select('age').where("name != Mike")
    self.assertEquals(len(people), 4)

  def test_searcher_with_not_equals_false_value_query(self):
    animals = self.searcher.fromClass("Animal").where("mammal != False")
    hashes = [animal.__hash__() for animal in animals]
    self.assertTrue(self.human.__hash__() in hashes and self.cat.__hash__() in hashes and self.dog.__hash__() in hashes)

  def test_searcher_with_not_equals_false_value_count(self):
    animals = self.searcher.fromClass("Animal").where("mammal != False")
    self.assertEquals(len(animals), 3)


class TestBook(unittest.TestCase):
  def setUp(self):
    self.book = Book()
    self.person = Person()
    self.person.name = "Mike"
    self.person.age = 20
    person1 = Person()
    person1.name = "Jouhan"
    person1.age = 22
    person2 = Person()
    person2.name = "Alex"
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
    self.assertEqual(['Alex', 'Jouhan', "Mike"], list(self.book.indexdb['Person']['name'].keys()))

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
    self.assertTrue(mike.__hash__() in self.book.indexdb['Person']['name']['Tim'].keys())
    self.assertTrue(mike.__hash__() not in self.book.indexdb['Person']['name']['Mike'].keys())

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

