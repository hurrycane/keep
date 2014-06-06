from .client import Client

from .adapter import AsyncHTTPAdapter
from .response import AsyncEtcdResponse

import requests
import gevent

class AsyncClient(Client):

  def __init__(self, host=None, port=None, peers=None, discovery=None,
               debug=False, adapter=AsyncHTTPAdapter, response_class=AsyncEtcdResponse):
    super(AsyncClient, self).__init__(host, port, peers, discovery, debug,
                                      adapter=AsyncHTTPAdapter,
                                      response_class=AsyncEtcdResponse)

  def _get_peers_by_discovery(self):
    print "D"
    pass
  
  """
  Ping is synchronous
  """
  def ping(self):
    self._execute_command('GET', "machines", None, expected_status=200,
                          expect_json=False).get()

  def watch(self, name, recursive=False):
    while True:
      try:
        print "^"
        response = self._execute_command('GET', "keys", "%s?wait=true&recursive=%s" % (name, recursive), timeout=0.5).get(timeout=0.75)
        yield response
      except requests.exceptions.Timeout:
        print "@"
      except gevent.Timeout:
        print "!"
