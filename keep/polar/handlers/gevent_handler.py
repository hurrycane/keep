import atexit

from gevent.queue import Empty
from gevent.queue import Queue
import gevent.event

from requests import Session

from keep.polar.parsers import JSONParser

_NONE = object()
_STOP = object()

GeventAsyncResult = gevent.event.AsyncResult

class AsyncResult(GeventAsyncResult):

  def __init__(self, handler, parser_klass=JSONParser):
    super(AsyncResult, self).__init__()

    self._handler = handler
    self._parser = parser_klass()

  def set(self, value):
    if self._parser:
      data, stats = self._parser.parse(value)
    else:
      data, stats = value, None

    super(AsyncResult, self).set((data,stats))

  @property
  def parser(self):
    return self._parser

  @parser.setter
  def parser(self, value):
    self._parser = value


class GeventHandler(object):
  timeout_exception = gevent.event.Timeout
  queue_impl = Queue
  queue_empty = Empty

  def __init__(self):
    self._workers = []

    self.callback_queue = self.queue_impl()

  def requests_impl(self):
    return Session()

  def _create_greenlet_worker(self, queue, queue_name):
    def greenlet_worker():
      while True:
        try:
          job = queue.get()

          if job is _STOP:
            break

          func, async_object = job
          result = func()

          if async_object:
            async_object.set(result)

        except self.queue_empty:
          continue

    return gevent.spawn(greenlet_worker)

  def start(self):
    w = self._create_greenlet_worker(self.callback_queue, "Watchers")
    self._workers.append(w)

    atexit.register(self.stop)

  def stop(self):

    for queue in (self.callback_queue, ):
      queue.put(_STOP)

    self._workers.reverse()

    while self._workers:
      worker = self._workers.pop()
      worker.join()

    self.callback_queue = self.queue_impl()

    if hasattr(atexit, "unregister"):
      atexit.unregister(self.stop)

  def async_result(self):
    return AsyncResult(self)

  def spawn(self, func, *args, **kwargs):
    return gevent.spawn(func, *args, **kwargs)
