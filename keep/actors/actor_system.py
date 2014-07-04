"""
What is the purpose of this Actor system?
To have an actor that reads from Queue for different kind of events.

when it receives a message it delegates it to the proper actor.
Each actors runs into it's own greenlet and it blocks async.
Each message is sent async.

--> queue --> routing --> actor.
                      --> actor.

Only one instance of Actor per context is permited - yes
"""

import gevent
from gevent.queue import Queue

from keep.actors import ActorContext, RootActor, ActorTree

_STOP = object()

class ActorRouting(object):

  def __init__(self, actor_system, name):
    self.system = actor_system
    self.actor_tree = ActorTree()

  @property
  def tree(self):
    return self.actor_tree

  #def actor_selection(self, path):
  #  self.actor_tree.select(path)

class ActorSystem(object):
  """
  Keeps track of the whole actor lifecycle
  """

  def __init__(self, polar_client, name):
    self._client = polar_client
    self._actor_name = name

    self._actor_routing = ActorRouting(self, name)

    self._create_root_actor()

    self._queue = self._client.Queue("actors-%s" % self._actor_name)
    self._spawn(self._inbox_handler)

  def _spawn(self, func, *args, **kwargs):
    gevent.spawn(func, *args, **kwargs)

  def _inbox_handler(self):
    while True:
      item = self._queue.get()
      print "ActorSystemInbox %s" % item

  def actor_of(self, actor_class):
    return self._spawn_actor(self.context, actor_class)

  def _create_root_actor(self):
    root_ref = self._actor_routing.tree.root
    context = ActorContext(root_ref, self)

    actor = RootActor(context)

    greenlet = self._spawn(self._actor_coroutine, actor)
    root_ref.greenlet = greenlet

    self.context = context

  def actor_selection(self, path):
    return self.context.ref.actor_selection(path)

  def _spawn_actor(self, context, actor_class):
    # ref <-|-> context <-|-> actor -> queue

    new_ref = context.ref.create_child_ref()
    new_ref.context = ActorContext(new_ref, self)

    kwargs = actor_class._props
    kwargs["context"] = new_ref.context

    actor = actor_class(**kwargs)

    greenlet = self._spawn(self._actor_coroutine, actor)
    new_ref.greenlet = greenlet

    return new_ref

  def _actor_coroutine(self, actor):
    while True:
      item = actor.queue.get()

      # death pill
      if item == _STOP:
        break

      actor.on_receive(item)
