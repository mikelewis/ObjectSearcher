from indexable import Indexable
from searcher import Searcher


class Post(Indexable):
  title = None
  body = None
  author = None
  numComments = 0
  indexableAttrs = ('author', 'numComments', )
  def __init__(self, title, body, author):
    Indexable.__init__(self)
    self.title = title
    self.body = body
    self.author = author

class Course(Indexable):
  name = None
  college = None
  professor = None
  indexableAttrs = ('college', 'professor', )
  def __init__(self, name, college, professor):
    Indexable.__init__(self)
    self.name = name
    self.college = college
    self.professor = professor

class Animal(Indexable):
  kind = None
  color = None
  owner = None
  indexableAttrs = ('kind', 'color',)
  def __init__(self, kind, color, owner):
    Indexable.__init__(self)
    self.kind = kind
    self.color = color
    self.owner = owner


#Add class to global scope to allow searcher.py to have access to these class names
# This is needed because of this interactive demo

c1 = Course(name="Database Concepts", college="GCCIS", professor="Raj")
c2 = Course(name="Database Security", college="GCCIS", professor="Hank")
c3 = Course(name="Graph Theory", college="COS", professor="Jacobs")
c4 = Course(name="Discrete Math 1", college="COS", professor="Ben")

a1 = Animal(kind="Cat", color="Red", owner="Mike")
a2 = Animal(kind="Dragon", color="Purple", owner="Jouhan")
a3 = Animal(kind="Bunny", color="Pink", owner="Alex")
a4 = Animal(kind="Panda", color="Yellow", owner="Timmy")

p1 = Post(title="First day at College", body="Soooo its been ok so far", author="Casie")
p1.numComments = 6
p2 = Post(title="Last day at school", body="I'm Done!!!!", author="Casie")
p2.numComments = 20
p3 = Post(title="Gracies is terrible", body="NEVER EAT THERE!!!", author="Mike")
p3.numComments = 25

searcher = Searcher()


# Credit to effbot.org/librarybook/code.htm for loading variables into current namespace
def keyboard(banner=None):
    import code, sys

    # use exception trick to pick up the current frame
    try:
        raise None
    except:
        frame = sys.exc_info()[2].tb_frame.f_back

    # evaluate commands in current namespace
    namespace = frame.f_globals.copy()
    namespace.update(frame.f_locals)

    code.interact(banner=banner, local=namespace)

def start():
  print "=" * 80
  print "-PLEASE EXIT USING CTRL-D, OTHERWISE THE DATABASE WILL NOT EXIST PROPERLY (ZODB ISSUE)"
  print "-This is an interactive python shell setup with an already setup searcher, and three classes to play around with (Animal, Course, Post)."
  print "-To access the searcher instance variable, the variable is searcher"
  print "- If you want to modify the created variables, they are c1-c4, a1-4, p1-3"
  print "-An example query: searcher.fromClass(\"Post\").select('title, numComments').where('numComments BETWEEN 10 AND 25')"
  print "- OR "
  print "=" * 80
  print "\n\n\n\n"
  keyboard()
  searcher._book.destroy_index()
  print "END"


if __name__ == '__main__':
  start()
