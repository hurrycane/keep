from gevent.pool import Pool
from gevent.queue import Queue

from gevent.timeout import Timeout

class RequestExecutor(object):

  def __init__(self, client, pool_size=20):
    self.client = client
    self.handler = client.handler

    self._queue = Queue()
    self._completion_queue = Queue()

    self._pool = Pool(20)

  def start(self):
    self._connection_routine = self.handler.spawn(self._executor_loop)
    self._completion_routine = self.handler.spawn(self._completion_loop)

  @property
  def queue(self):
    return self._queue

  def _executor_loop(self):
    while True:
      item = self._queue.get()

      request, async_result = item

      greenlet = self._pool.spawn(lambda: request())
      self._completion_queue.put((greenlet, async_result))

  def _completion_loop(self):
    while True:
      item = self._completion_queue.get()

      greenlet, async_result = item

      while True:
        try:
          result = greenlet.get(timeout=1)

          break
        except Timeout:
          pass

      async_result.set(result)
