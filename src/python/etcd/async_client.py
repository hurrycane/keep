from .client import Client

from .adapter import AsyncHTTPAdapter
from .response import AsyncEtcdResponse

class AsyncClient(Client):

  def __init__(self, host=None, port=None, peers=None, discovery=None,
               debug=False, adapter=AsyncHTTPAdapter, response_class=AsyncEtcdResponse):

    super(AsyncClient, self).__init__(host, port, peers, discovery, debug,
                                      adapter=AsyncHTTPAdapter,
                                      response_class=AsyncEtcdResponse)

  def _get_peers_by_discovery(self):
    pass

  def _ping(self):
    pass
