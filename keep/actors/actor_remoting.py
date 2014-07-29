import gevent

from urlparse import urlparse

class ActorRemoting(object):
  def __init__(self, polar_client, actor_system):
    self._client = polar_client
    self._actor_system = actor_system

    self._actor_name = self._actor_system._actor_name

  def start(self):
    self._queue = self._client.Queue("actors-%s" % self._actor_name)

    gevent.spawn(self._start)

  def _start(self):
    while True:
      item = self._queue.get()
      print "@@@@@@@@@@@@@@@@@@@@@@@@ Item from remoting - %s" % item

  def tell(self, remote_uri, message_body):
    parsed_uri = urlparse(remote_uri)

    print "!!!!!!!!!!!!!!! Writing to queue - %s" % parsed_uri.netloc

    self._client.WriteOnlyQueue("actors-%s" % parsed_uri.netloc).put(message_body)

  def ask(self, message_body):
    pass
