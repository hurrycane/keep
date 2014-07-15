from urlparse import urlparse

from gevent.queue import Queue

class ActorMessaging(object):

  def __init__(self, hierarchy):
    self._hierarchy = hierarchy

    self._asking_queues = {}

  def tell(self, absolute_path, message):
    uri = urlparse(absolute_path)

    if uri.scheme:
      # pick hostname and put into that queue
      print "Looking remote"
    else:
      for context in self._hierarchy.actor_selection(absolute_path):
        context.actor.queue.put(message)

  def ask(self, absolute_path, message):
    self._asking_queues[ message["ask-id"] ] = Queue(maxsize=1)

    uri = urlparse(absolute_path)

    # TODO: Should be merged into one
    if uri.scheme:
      # pick hostname and put into that queue
      print "Looking remote"
    else:
      for context in self._hierarchy.actor_selection(absolute_path):
        context.actor.queue.put(message)
