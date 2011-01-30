from indexable import Indexable
from searcher import Searcher

class Car(Indexable):
  color=None
  brand=None
  year=None
  indexableAttrs = ('year', 'brand', 'color', )

  def __init__(self, color=None, brand=None, year=None):
    Indexable.__init__(self)
    self.color = color
    self.brand = brand
    self.year = year

  def __str__(self):
    return self.color + " " + self.brand + " built in " + str(self.year)



if __name__ == '__main__':
  c1 = Car("Red", "Ford", 1974)
  c2 = Car("Yellow", "Dodge", 2000)
  c3 = Car("Black", "Toyota", 2005)
  c4 = Car("Pink", "Chevy", 1985)
  c5 = Car("Red", "Ferrari", 1990)
  c6 = Car("Black", "Ford", 1990)

  searcher = Searcher()

  fordCars = searcher.fromClass("Car").where("brand = Ford")
  newCars = searcher.fromClass("Car").where("year >= 2000")
  blackFords = searcher.fromClass("Car").where("brand = Ford AND color = Black ")
  blackOrRedCars = searcher.fromClass("Car").where("color = Red OR color = Black")
  redOrFerrariCars = searcher.fromClass("Car").where("color = Red OR brand = Ferrari")

  print "====Ford Cars==="
  for car in fordCars:
    print car

  print "====Cars made in 2000 or later==="
  for car in newCars:
    print car

  print "====Black Fords==="
  for car in blackFords:
    print car

  print "====Black or Red Cars==="
  for car in blackOrRedCars:
    print car

  print "====Black or Red Cars==="
  for car in redOrFerrariCars:
    print car
