class WriteOnlyQueue(object):

  def __init__(self, client, name, maxsize=512):
    self.client = client

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

  def put(self, item):
    return self.client.mknod_async("queue-%s" % self.queue_name, item)
