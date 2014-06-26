import atexit
import threading

import Queue

from requests import Session

from keep.polar.parsers import JSONParser

_NONE = object()
_STOP = object()

class TimeoutError(Exception):
  pass

class AsyncResult(object):

  def __init__(self, handler, parser_klass=JSONParser):
    self._handler = handler
    self.value = None
    self._exception = _NONE
    self._condition = threading.Condition()
    self._callbacks = []

    self._parser = parser_klass()

  def ready(self):
    return self._exception is not _NONE

  def successful(self):
    return self._exception is None

  @property
  def exception(self):
    if self._exception is not _NONE:
      return self._exception

  def set(self, value=None):
    with self._condition:

      if self._parser:
        data, stats = self._parser.parse(value)
      else:
        data, stats = value, None

      self.value = (data, stats)
      self._exception = None

      for callback in self._callbacks:
        self._handler.completion_queue.put(
          (
            lambda: callback(self),
            None
          )
        )

      self._condition.notify_all()

  def set_exception(self, exception):
    """Store the exception. Wake up the waiters."""
    with self._condition:
      self._exception = exception

      #for callback in self._callbacks:
      #  self._handler.completion_queue.put(
      #    lambda: callback(self)
      #  )

      self._condition.notify_all()

  def get(self, block=True, timeout=None):
    with self._condition:

      if self._exception is not _NONE:

        if self._exception is None:
          return self.value

        raise self._exception

      elif block:
        self._condition.wait(timeout)
        if self._exception is not _NONE:

          if self._exception is None:
            return self.value

          raise self._exception

      # if we get to this point we timeout
      raise TimeoutError()

  def get_nowait(self):
    return self.get(block=False)

  def wait(self, timeout=None):
    with self._condition:
      self._condition.wait(timeout)

    return self._exception is not _NONE

  def rawlink(self, callback):
    with self._condition:
      # Are we already set? Dispatch it now
      if self.ready():
        self._handler.completion_queue.put(
          lambda: callback(self)
        )
        return

      if callback not in self._callbacks:
        self._callbacks.append(callback)

  def unlink(self, callback):
    with self._condition:
      if self.ready():
        # Already triggered, ignore
        return

      if callback in self._callbacks:
        self._callbacks.remove(callback)

  @property
  def parser(self):
    return self._parser

  @parser.setter
  def parser(self, value):
    self._parser = value

class ThreadingHandler(object):
  timeout_exception = TimeoutError
  queue_impl = Queue.Queue
  queue_empty = Queue.Empty

  def __init__(self):
    self._workers = []

    # callback_queue
    self.callback_queue = self.queue_impl()

    # setter queue + callbacks
    self.completion_queue = self.queue_impl()

  def requests_impl(self):
    return Session()

  def _create_thread_worker(self, queue, queue_name):
    def thread_worker():
      while True:
        try:
          func, async_object = queue.get()

          if func is _STOP:
            break

          #print "Started %s with func = %s" % (queue_name, func)
          result = func()
          #print "Ended %s with func = %s" % (queue_name, func)

          if async_object:
            async_object.set(result)

        except self.queue_empty:
          continue

    t = threading.Thread(target=thread_worker)
    t.start()

    return t

  def start(self):
    #for queue in (self.completion_queue, self.callback_queue):
    w = self._create_thread_worker(self.completion_queue, "Callbacks")
    self._workers.append(w)

    w = self._create_thread_worker(self.callback_queue, "Watchers")
    self._workers.append(w)

    atexit.register(self.stop)

  def stop(self):

    for queue in (self.completion_queue, self.callback_queue):
      queue.put(_STOP)

    self._workers.reverse()

    while self._workers:
      worker = self._workers.pop()
      worker.join()

    self.callback_queue = self.queue_impl()
    self.completion_queue = self.queue_impl()

    if hasattr(atexit, "unregister"):
      atexit.unregister(self.stop)

  def async_result(self):
    return AsyncResult(self)
