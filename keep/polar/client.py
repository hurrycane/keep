from .handlers.threading_handler import ThreadingHandler

import random
from functools import partial

import requests
from gevent import sleep

from keep.polar.utils import retry
from keep.polar.protocol import Request, LifoQueue, Watcher
from keep.polar.protocol import RequestExecutor

"""
from polar.client import PolarClient

client = PolarClar(hosts=[])
client.start() # => fetch machines, make ping

data, stat = client.set("a", "b")

return types:
  key/value

  key -> node
  directory -> set

  events: create, delete, expire, what happend we lose qvorum ?
"""

class PolarClient(object):

  def __init__(self, hosts="http://127.0.0.1:4001", handler=None,
               timeout=10.0, randomize_hosts=True, fetch_hosts=True):

    self.hosts = hosts
    self.current_hosts = self.hosts

    self.handler = handler if handler else ThreadingHandler()
    self.fetch_hosts = fetch_hosts

    self.timeout = timeout
    self.randomize_hosts = randomize_hosts

    self._request_executor = RequestExecutor(client=self)
    self._queue = self._request_executor.queue

  def start(self):
    # ping
    self.handler.start()
    self._request_executor.start()

    self.ping()

    if self.fetch_hosts:
      self.fetch_machines()

    sleep(2)

  def fetch_machines(self):
    async_result = self.handler.async_result()
    async_result.parser = None

    self._call(Request("GET", "/v2/machines"), async_result)

    @retry(exception=self.handler.timeout_exception, times=3, backoff=5)
    def callback(result):
      # if after two seconds doesnt' finish ?
      machines, stats = result.get(timeout=2)
      self.hosts = machines.text.split(",")

    async_result.rawlink(callback)

  def set_async(self, path, value):
    async_result = self.handler.async_result()
    self._call(Request("PUT", "/v2/keys/%s" % path, data={
      "value": value
    }), async_result)

    return async_result

  def set(self, path, value):
    return self.set_async(path, value).get()

  def get_async(self, path, watch):
    async_result = self.handler.async_result()
    request = Request("GET", "/v2/keys/%s" % path)

    self._call(request, async_result)

    # if there is a watch here put into the watcher queue.

    if watch:
      self._watch(path, request, watch)

    return async_result

  def get(self, path, watch=None):
    return self.get_async(path, watch).get()

  def get_children_async(self, path, watch=None):
    async_result = self.handler.async_result()
    request = Request("GET", "/v2/keys/%s" % path, query=["recursive=true", "sorted=true"])

    self._call(request, async_result)

    if watch:
      self._watch(path, request, watch, is_dir=True)

    return async_result

  def get_children(self, path, watch=None):
    return self.get_children_async(path, watch).get()

  def ping_async(self):
    async_result = self.handler.async_result()
    async_result.parser = None

    self._call(Request("GET", "/v2/stats/self"), async_result)

    return async_result

  def ping(self):
    return self.ping_async().get()

  def mkdir_async(self, path):
    async_result = self.handler.async_result()

    self._call(Request("PUT", "/v2/keys/%s" % path, data={
      'dir': True
    }), async_result)

    return async_result

  def mkdir(self, path):
    return self.mkdir_async(path).get()

  def delete_async(self, path):
    async_result = self.handler.async_result()
    async_result.parser = None

    self._call(Request("DELETE", "/v2/keys/%s" % path), async_result)

    return async_result

  def delete(self, path):
    self.delete_async(path).get()

  def cas_async(self, path, future_value, prev_value):
    async_result = self.handler.async_result()

    self._call(
      Request(
        "PUT",
        "/v2/keys/%s" % path,
        [ "prevValue=%s" % prev_value ],
        data={ "value": future_value},
      ),
      async_result
    )

    return async_result

  def cas(self, path, future_value, prev_value):
    return self.cas_async(path, future_value, prev_value).get()

  def _get_wait_index(self, stats):
    if "nodes" in stats["node"]:
      pass
    else:
      pass
      # is dir and is sorted

  def watch(self, path, watch_func, wait_index=None, is_dir=False):
    request = Request(
      "GET",
      "/v2/keys/%s" % path,
      query=["recursive=true", "sorted=true"]
    )

    self._watch(path, request, watch, wait_index=None, is_dir=is_dir)

  def _watch(self, path, request, watch_func, wait_index=None, is_dir=False):
    return Watcher(self, path, request, watch_func, wait_index, is_dir)

  def _prepare(self, request):
    """
    Returns the partial function that can be run into a greenlet.
    """
    session = self.handler.requests_impl()
    peer = self._get_peer()

    if not peer.startswith("http"):
      peer = "http://%s" % peer

    query_string = "&".join(request.query if request.query else [])

    url = "%s%s?%s" % (peer, request.url, query_string)

    return partial(session.request, request.method, url, data=request.data)

  def _call(self, request, async_object):
    prepared = self._prepare(request)

    print request.method, request.url, request.query, request.data
    self._queue.put((prepared, async_object))

  def _get_peer(self):
    if self.randomize_hosts == True:
      hosts = self.hosts
    else:
      hosts = self.current_hosts

    return random.sample(hosts, 1)[0]

  def Queue(self, name):
    return LifoQueue(self, name)
