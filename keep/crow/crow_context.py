"""
Crow manages the list of hosts in the cluster.
"""

import gevent

CROW_TIMEOUT = 0.5

class CrowContext(object):

  def __init__(self, polar_client, hostname, cluster="prod"):
    self.client = polar_client
    self.hostname = hostname
    self.cluster = cluster

    self.crow_key = "crow-hostnames-%s" % cluster

    node, stats = self.client.get(self.crow_key)

    if node != None and type(node) != list:
      raise AttributeError("The key %s already exists and is not a directory" % self.crow_key)

    if node == None:

      node, stats = self.client.mkdir(self.crow_key)

    self.client.watch("crow-hostnames-%s" % cluster, self._crow_watch, is_dir=True)
    self.hosts = set()

    self._started = False
    self.default_ttl = 3

  def announce(self):
    self._started = True
    gevent.spawn(self._refresh_ttl)

  def _refresh_ttl(self):
    while self._refresh_ttl:
      self.client.set("%s/%s" % (self.crow_key, self.hostname), self.hostname,
                      ttl=self.default_ttl)

      gevent.sleep(CROW_TIMEOUT)

  def _crow_watch(self, result):
    value, stats = result
    #print "Watching for changes %s" % value
    #print stats["action"], stats["node"]["key"], stats["node"]["value"]

    if stats["action"] == "expire":
      print stats
