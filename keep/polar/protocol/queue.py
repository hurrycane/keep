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

from Queue import Queue

class LifoQueue(object):

  def __init__(self, client, name, maxsize=512):
    """
    When you start a queue you create a watcher that just puts each
    new node into the Queue.
    """

    self.client = client
    self.queue = Queue(maxsize)

    # check if key exists otherwise get it
    node, stats = self.client.get("queue/%s" % name)

    if node == None:
      self.client.mkdir("queue/%s" % name)

    _, stats = self.client.set("queue/%s/_last_modified_index" % name, -1)

    wait_index = stats["node"]["modifiedIndex"]

    nodes, stats = self.client.get_children("queue/%s" % name, self._watch)

    for node in nodes:
      self.client.delete_async(node["key"][1:])
      self.queue.put(node["value"])

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

  def _watch(self, result):
    value, stats = result

    if stats["action"] == "create":
      self.client.delete_async(stats["node"]["key"][1:])
      self.queue.put(value)
