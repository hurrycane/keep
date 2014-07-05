"""
Crow manages the list of hosts in the cluster.
"""

import time
import gevent

import logging

from collections import deque

from . import set_up_logging

set_up_logging("crow")
log = logging.getLogger("crow")

from .phi_accrual_failure_detector import AccuralFailureDetector
from .exceptions import NotEnoughData

CROW_TIMEOUT = 0.5
CROW_PHI_TIMEOUT = 0.7

class CrowContext(object):

  def __init__(self, polar_client, hostname, cluster="prod"):
    self.client = polar_client
    self.hostname = hostname
    self.cluster = cluster

    self.crow_key = "crow-hostnames-%s" % cluster
    # create keys if they are not present
    self._create_keys()

    self.heartbeat_history = {}
    self._started = False
    self.default_ttl = 3
    self._hosts = set()

    # start watcher
    self.client.watch("crow-hostnames-%s" % cluster, self._crow_watch, is_dir=True)

  def _create_keys(self):
    node, stats = self.client.get(self.crow_key)

    if node != None and type(node) != list:
      raise AttributeError("The key %s already exists and is not a directory" % self.crow_key)

    if node == None:
      node, stats = self.client.mkdir(self.crow_key)

  @property
  def hosts(self):
    return self._hosts

  def add_handler(self, event, handler):
    pass

  def _compute_phi(self):
    while True:
      for key in self.heartbeat_history.keys():

        if key == self.hostname:
          continue

        # the phi failure detector
        try:
          failure_detector = AccuralFailureDetector(self.heartbeat_history[key])
          time_from_last_seen = time.time() - self.heartbeat_history[key][-1]

          phi = failure_detector.phi(time_from_last_seen)

          if phi > 5.3 and phi < 20:
            if key in self._hosts:
              log.info("Host %s removed from list", key)
              self._hosts.discard(key)
          elif phi >= 20:
            del self.heartbeat_history[key]
            log.info("Host %s removed from general list", key)
          else:
            if key not in self._hosts:
              log.info("Host %s added", key)
              self._hosts.add(key)

        except NotEnoughData:
          pass

      gevent.sleep(CROW_PHI_TIMEOUT)

  def announce(self):
    self._started = True
    gevent.spawn(self._refresh_ttl)
    gevent.spawn(self._compute_phi)

  def _refresh_ttl(self):
    while self._refresh_ttl:
      self.client.set("%s/%s" % (self.crow_key, self.hostname), self.hostname,
                      ttl=self.default_ttl)

      gevent.sleep(CROW_TIMEOUT)

  def _crow_watch(self, result):
    value, stats = result

    if stats["action"] == "set":
      key_with_hostname = stats["node"]["key"]
      hostname = key_with_hostname.split("/")[-1]

      if hostname not in self.heartbeat_history:
        self.heartbeat_history[hostname] = deque()

      self.heartbeat_history[hostname].append(time.time())

      if len(self.heartbeat_history[hostname]) > 100:
        self.heartbeat_history[hostname].popleft()
