class ActorRef(object):

  def __init__(self, parent):
    self.children = []
    self.parent_ref = parent

  def create_child_ref(self):
    # self.children
    new_ref = ActorRef(self)
    self.children.append(new_ref)

    return new_ref

  @property
  def greenlet(self):
    return self._greenlet

  @greenlet.setter
  def greenlet(self, value):
    self._greenlet = value

class ActorTree(object):

  def __init__(self):
    self._root = ActorRef(parent=None)

  @property
  def root(self):
    return self._root

  def select(path):
    return None
