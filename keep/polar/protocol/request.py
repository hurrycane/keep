from collections import namedtuple

class Request(namedtuple('Request', ['method', 'url', 'query', 'data'])):
  def __new__(cls, method, url, query=None, data=None):

    if data == None:
      data = {}

    return super(Request, cls).__new__(cls, method, url, query, data)
