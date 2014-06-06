import random

from .response import EtcdResponse
from .adapter import HTTPAdapter

import requests

class StatusCodeException(Exception):
  pass

class Client(object):

  def __init__(self, host=None, port=None, peers=None, discovery=None,
               debug=False, adapter=HTTPAdapter, response_class=EtcdResponse):

    self.adapter = adapter()
    self.response_class = response_class

    if host and port:
      # TODO: If a peer fails than refresh the whole peers list.
      self.peers = [ { "host": host, "port": port } ]
    elif peers and all(self.peers, lambda peer: peer["host"] and peer["port"]):
      self.peers = peers
    elif discovery and discovery.startswith("http://"):
      self.peers = self._get_peers_by_discovery(discovery)
    else:
      raise AttributeError("Provide either host, port, peers or discovery\
                           token")

    self.next_peer = 1
    self.ping()

  def _get_peers_by_discovery(self, discovery):
    response = self.adapter.get(discovery)

    try:
      peers = []
      for peer in response["node"]["nodes"]:
        host = peer["value"][7:].split(":")

        peers.append({
          "host": host[0],
          "port": host[1]
        })

      return peers
    except:
      raise AttributeError("Discovery response is malformed")

  def ping(self):
    self._execute_command('GET', "machines", None, expected_status=200,
                          expect_json=False)

  def get(self, name, consistent=True):
    return self._execute_command('GET', "keys", name)

  def set(self, name, value, ttl=None, consistent=True):
    data = { 'value': value }
    if ttl:
      data['ttl'] = ttl

    return self._execute_command('PUT', "keys", name, data)

  def mkdir(self, name, value=None, ttl=None, full=False, consistent=True):
    data = { 'dir': True }

    if not ttl:
      data['ttl'] = ttl

    if value == None:
      value = "keys"

    return self._execute_command('PUT', value, name, data, no_answer=True,
                                 full=True)

  def listdir(self, name, recursive=False):
    return self._execute_command('GET', "keys", "%s/?recursive=%s" % (name, recursive),
                                 full=True)


  def delete(self, name, full=False):
    return self._execute_command('DELETE', "keys", name, no_answer=True,
                                 full=full)

  def refresh_dir(self, name):
    pass

  def refresh(self, name, ttl, value=None, full=False):
    data = { 'prevExist': True }

    if value:
      data['value'] = value

    if ttl:
      data['ttl'] = ttl

    return self._execute_command('PUT', "keys", name, data,
                                 full=Full)

  def watch(self, name, recursive=False):
    while True:
      try:
        response = self._execute_command('GET', "keys", "%s?wait=true&recursive=%s" % (name, recursive))
        yield response
      except requests.exceptions.Timeout:
        pass

  def lock(self, ket, ttl=60, index=None):
    pass

  def _base_url(self, peer):
    return "http://%s:%s/v2" % (peer["host"], peer["port"])

  def _get_peer(self):
    self.next_peer = random.randint(1, len(self.peers))
    return self.peers[self.next_peer-1]

  def _prepare_url(self, prefix, path):
    peer = self._get_peer()
    url = "%s/%s" % (self._base_url(peer), prefix)

    if path:
      url += "/%s" % path

    return url

  """executes the actual HTTP request
  :param verb: http_verb one of GET, POST, PUT, DELETE
  :param prefix:
  :param path:
  :param data: dict (key/value pairs) that makes the request body (in case of
               POST/PUT)
  :param timeout: Timeout for waiting for requests - passed to requests.
                  Default value is 5s.
  :param expected_status: You can validate the response by validating the
                          response status of the request.
  :param expect_json: There are some edge cases in etcd when the response
                      is not json so we need to parse it separatly.
  """
  def _execute_command(self, verb, prefix, path, data=None, timeout=5,
                       expected_status=None, expect_json=True):

    url = self._prepare_url(prefix, path)
    response = self.adapter.do_request(verb, url, data, timeout)
    return self.response_class(response, expected_status, expect_json)

  #partial_request = self._prepare_request(verb, prefix, path, data, timeout)
  #  response = partial_request()

  #  if expected_status:
  #    if type(expected_status) != list and type(expected_status) != set:
  #      expected_status = [ expected_status ]

  #    if response.status_code not in expected_status:
  #      raise StatusCodeException("Status code mismatch expected %s but got %s" % (expected_status, response.status_code))

  #  return self._parse_response(response, full=full, no_answer=no_answer)
