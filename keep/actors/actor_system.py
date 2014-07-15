"""
What is the purpose of this Actor system?
To start different services that manage message passing for local and
remote actors.
"""

import gevent
from gevent.queue import Queue

from keep.actors import ActorHierarchy, ActorExecutor, ActorRemoting
from keep.actors import ActorMessaging
from keep.actors import RootActor

_STOP = object()

class ActorSystem(object):
  """
  Starts and configures different components
  """

  def __init__(self, polar_client, name, hierarchy_class=ActorHierarchy,
               executor_class=ActorExecutor, remoting_class=ActorRemoting,
               messaging_class=ActorMessaging):

    self._client = polar_client
    self._actor_name = name

    self._actor_hierarchy = hierarchy_class(self)
    self._actor_messaging = messaging_class(self._actor_hierarchy)

    self._actor_executor = executor_class(self._actor_messaging)
    self._actor_remoting = remoting_class(self._client, self)

    self._init_system()
    #self._queue = self._client.Queue("actors-%s" % self._actor_name)
    #self._spawn(self._inbox_handler)

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    pass
    #self._actor_executor.join()

  def actor_of(self, actor_class):
    return self.context.actor_of(actor_class)

  def _init_system(self):
    """
    Creates a RootActor - inits the hierarchi and creates a context
    for the actor system.
    """

    self._context = self._actor_hierarchy.init(RootActor)

  def actor_selection(self, query):
    return self.context.actor_selection(query)

  @property
  def context(self):
    return self._context

  @property
  def executor(self):
    return self._actor_executor
