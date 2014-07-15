"""
Queue over etcd protocol

e.g.

polar_client = PolarClient(hosts=[])
queue = polar_client.Queue(named_queue) # Queue is an alias for LifoQueue
queue = polar_client.PriorityQueue(named_queue, size=100)

queue.get
queue.put
queue.empty
queue.full

When I read from the Queue I create an key with TTL in a separate directory.
When I read a key i check it on that directory. If it exists it means
that the item is reserved.
"""

import random
from functools import partial

import requests

import gevent
from gevent import socket
from gevent.queue import Queue

from keep.polar.protocol import Request
from keep.polar.exceptions import StaleData

class LifoQueue(object):

  def __init__(self, client, name, maxsize=512):
    """
    When you start a queue you create a watcher that just puts each
    new node into the Queue.
    """

    self.client = client
    self.handler = client.handler
    self.queue = Queue(maxsize)

    self.queue_name = "queue-body-%s" % name
    self.queue_head = "queue-heads-%s" % name

    # check if key exists otherwise create it
    node, stats = self.client.get(self.queue_name)

    head_index = None

    # Problem: what happens when head_index is screwed
    # and we want to revert it. If we find it not parseable
    # we se it to the latest etcd index

    if node != None:
      head_index, stats = self.client.get(self.queue_head)

      try:
        head_index = int(head_index)
      except ValueError:
        head_index = int(stats["stats"]["X-Etcd-Index"])

    else:
      node, stats = self.client.mkdir(self.queue_name)
      self.client.set(self.queue_head, stats["node"]["modifiedIndex"])

      head_index = stats["node"]["modifiedIndex"]

    result = self.handler.async_result()
    result.parser = None

    self.client.handler.callback_queue.put((
      partial(self._start, head_index), result
    ))

  def _start(self, head_index):
    request = Request("GET", "/v2/keys/%s" % self.queue_name,
                      query=[
                        "wait=true",
                        "waitIndex=%s" % (int(head_index)+1),
                        "recursive=true"
                      ])

    url, prepared = self.client._prepare_s(request)

    try:
      timeout = random.randint(500, 600)
      result = prepared(timeout=timeout/100.0)

      parser = self.handler.async_result().parser
      item = parser.parse(result)

      queue_item, stats = item

      # it should be an add, if it is with the head that you have right now
      # try to change the head to the modifiedIndex if you succed
      # than you have the element

      if stats["action"] != "create":
        return

      new_head_index = stats["node"]["modifiedIndex"]
      value, stats = self.client.cas(self.queue_head, new_head_index, head_index)

      # if CAS failed
      if value == None and stats["errorCode"] == 101:
        split_cause = stats["cause"][1:-1].split(" ")

        if int(split_cause[0]) == head_index:
          head_index = int(split_cause[-1])
        else:
          head_index = int(split_cause[0])

      else:
        head_index = new_head_index

        self.queue.put((queue_item, stats))

    except requests.exceptions.Timeout:
      pass
    except gevent.Timeout:
      print "Timed out!"
    except StaleData:
      _, stats = self.client.get("")
      wait_index = int(stats["stats"]["X-Etcd-Index"])
    except socket.timeout:
      pass
    finally:
      self.client.handler.callback_queue.put((
        partial(self._start, head_index),
        self.handler.async_result()
      ))

  def get(self, block=True, timeout=None):
    return self.queue.get(block, timeout)

  def get_nowait(self):
    return self.queue.get_nowait()
    # can raise Empty right away

  def put(self, item, block=True, timeout=None):
    # block until a free spot is available
    return self.client.mknode_async("queue-%s" % name, item)

  def join(self):
    pass

  def task_done(self):
    pass
