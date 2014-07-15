import xml.etree.ElementTree as ET

from .actor_context import ActorContext

class ActorHierarchy(object):

  def __init__(self, actor_system):
    self._actor_system = actor_system
    self._root = None

  @property
  def root(self):
    return self._root

  def init(self, root_actor_class):
    self._root = ActorContext(actor_system=self._actor_system,
                              parent_context=None)

    actor = self._actor_system.executor.spawn(root_actor_class, self._root)
    self._root.actor = actor

    self._root_element = ET.ElementTree(self._root.element)

    return self._root

  def context_selection(self, query):
    return [ item.get('context') for item in self._root_element.findall(query) ]

  def raw_actor_selection(self, query):
    return self._root_element.findall(query)
