import random
import requests

class StatusCodeException(Exception):
  pass

class Client(object):

  def __init__(self, host=None, port=None, peers=None, discovery=None,
               debug=False):

    if host and port:
      self.peers = [ { "host": host, "port": port } ]
    elif peers and all(self.peers, lambda peer: peer["host"] and peer["port"]):
      self.peers = peers
    elif discovery and discovery.startswith("http://"):
      response = request.get(discovery)

      try:
        self.peers = []
        for peer in response["node"]["nodes"]:
          host = peer["value"][7:].split(":")

          self.peers.append({
            "host": host[0],
            "port": host[1]
          })

      except:
        raise AttributeError("Discovery response is malformed")

    else:
      raise AttributeError("Provide either host, port, peers or discovery\
                           token")

    self.next_peer = 1

    # Make a ping request to fail fast if no connectivity exists.
    self._execute_command('GET', "machines", None, no_answer=True,
                          expected_status=200)

  def get(self, name, full=False, consistent=True):
    return self._execute_command('GET', "keys", name, full=full)

  def set(self, name, value, full=False, ttl=None, consistent=True):
    data = { 'value': value }
    if ttl:
      data['ttl'] = ttl

    return self._execute_command('PUT', "keys", name, data,
                                 full=full)

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
        response = self._execute_command('GET', "keys", "%s?wait=true&recursive=%s" % (name, recursive), full=True)
        yield response
      except requests.exceptions.Timeout:
        pass

  def _base_url(self, peer):
    return "http://%s:%s/v2" % (peer["host"], peer["port"])

  def _parse_response(self, response, full=False, no_answer=False):
    if full == True:
      return response.json()
    else:
      if no_answer == True:
        return None

      return response.json()["node"]["value"]

  def _get_peer(self):
    self.next_peer = random.randint(1, len(self.peers))
    return self.peers[self.next_peer-1]

  def _prepare_request(self, verb, prefix, path, data, timeout):
    partial_requests = getattr(requests, verb.lower())

    peer = self._get_peer()
    url = "%s/%s" % (self._base_url(peer), prefix)

    if path:
      url += "/%s" % path

    if data == None:
      data = {}

    def do_request():
      return partial_requests(url, data=data, timeout=timeout)

    return do_request

  """executes the actual HTTP request
  :param verb: http_verb one of GET, POST, PUT, DELETE
  :param prefix:
  :param path:
  :param data: dict (key/value pairs) that makes the request body (in case of
               POST/PUT)
  :param full: returns the full response if provided.
  :param no_answer: all the requests responses are parsed unless no_answer is
                    provided
  :param timeout: Timeout for waiting for requests - passed to requests.
                  Default value is 60s.
  :param expected_status: You can validate the response by validating the
                          response status of the request.
  """
  def _execute_command(self, verb, prefix, path, data=None, full=False,
                       no_answer=False, timeout=60, expected_status=None):

    partial_request = self._prepare_request(verb, prefix, path, data, timeout)
    response = partial_request()

    if expected_status:
      if type(expected_status) != list and type(expected_status) != set:
        expected_status = [ expected_status ]

      if response.status_code not in expected_status:
        raise StatusCodeException("Status code mismatch expected %s but got %s" % (expected_status, response.status_code))

    return self._parse_response(response, full=full, no_answer=no_answer)
