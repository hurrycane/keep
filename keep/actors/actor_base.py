from copy import deepcopy

from gevent.queue import Queue
from actor_context import ActorContext

class Actor(object):

  _props = {}

  def __init__(self, context):
    self.context = context
    self.context.actor = self

    self.queue = Queue()

  def actor_selection(self, path):
    return self.context.ref.actor_selection(path)

  @classmethod
  def props(cls, **kwargs):
    copied_cls = deepcopy(cls)
    copied_cls._props = kwargs

    return copied_cls
