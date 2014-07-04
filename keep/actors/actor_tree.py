from urlparse import urlparse

class ActorRef(object):

  def __init__(self, parent):
    self.children = []
    self.parent_ref = parent
    self._context = None

  def create_child_ref(self):
    # self.children
    new_ref = ActorRef(self)
    self.children.append(new_ref)

    return new_ref

  def _selection_path(self, path):
    if path[0] == "/":
      find_root = lambda x: x if x.parent_ref == None else find_root(x.parent_ref)
      level = find_root(self)
    else:
      level = self

    path = filter(None, path.split("/"))

    for elem in path:
      if elem == "..":

        # if not root
        if level.parent_ref:
          # one level up
          level = level.parent_ref

      elif elem == "*":
        return level.children
      else:
        for actor_ref in level.children:
          if actor_ref.context.actor.__class__.__name__ == elem:
            level = actor_ref
            break

    return level

  def actor_selection(self, query):
    """
    Examples: /ceva/../altceva/*

    It returns ActorRefs
    """
    uri = urlparse(query)

    if uri.scheme:
      print "Looking remote"
    else:
      return self._selection_path(uri.path)

  @property
  def context(self):
    return self._context

  @context.setter
  def context(self, value):
    self._context = value

  def tell(self, message):
    self.context.actor.queue.put(message)

  def ask(self, message, block=True, timeout=-1):
    pass

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
