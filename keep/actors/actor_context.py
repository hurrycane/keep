import uuid

import xml.etree.ElementTree as ET

from .actor_ref import ActorRef

class ActorContext(object):
  """
  Responsible for the context of a single actor. Part of the ActorHierarchy
  """

  def __init__(self, actor_system, parent_context):
    self._actor_system = actor_system
    self._messaging = actor_system._actor_messaging

    self._parent_context = parent_context

    self._actor = None
    self._actor_id = str(uuid.uuid4())

    self._children = []

  @property
  def parent(self):
    return self._parent_context

  @property
  def actor(self):
    return self._actor

  @property
  def element(self):
    return self._element

  @actor.setter
  def actor(self, value):
    self._actor = value

    if self._parent_context == None:
      self._element = ET.Element('RootActor')
      self._absolute_path = ""
    else:
      class_name = value.__class__.__name__

      self._element = ET.SubElement(self._parent_context.element, "%s" % (
        class_name
      ), attrib={
        "context": self,
        "id": self._actor_id
      })

      self._absolute_path = "%s/%s[@id='%s']" % (
        self._parent_context._absolute_path,
        class_name,
        self._actor_id
      )

  def actor_selection(self, query):
    if query[0] == "/":
      result = self._actor_system._actor_hierarchy.raw_actor_selection(query)
    else:
      result = self._element.findall(query)

    return [ ActorRef(self, item.get("context")._absolute_path) for item in result ]

  def actor_of(self, actor_class):
    self._child_context = ActorContext(actor_system=self._actor_system,
                                       parent_context=self)

    actor = self._actor_system._actor_executor.spawn(
      actor_class=actor_class,
      context=self._child_context
    )

    self._children.append(self._child_context)

    return ActorRef(self, self._child_context._absolute_path)
