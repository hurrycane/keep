import requests
import grequests

class Adapter(object):
  def do_request(self, verb, url, data=None):
    pass

class HTTPAdapter(Adapter):

  def do_request(self, verb, url, data=None, timeout=5):
    partial = getattr(requests, verb.lower())
    return partial(url, data=data, timeout=timeout)

class AsyncHTTPAdapter(Adapter):

  def do_request(self, verb, url, data=None, timeout=5):
    partial = getattr(grequests, verb.lower())
    prepared = partial(url, data=data, timeout=timeout)
    return grequests.send(prepared)
