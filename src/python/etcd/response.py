import sys

class EtcdResponse(object):
  def __init__(self, response, expected_status, expect_json=True):
    try:
      self.response = response.json()
    except ValueError, ex:
      if expect_json == True:
        # NOTE: re-raising exceptions in Python oh-joy
        t, v, tb = sys.exc_info()
        raise t, v, tb

      self.response = response.text

    self._value = None

    if expected_status:
      if type(expected_status) != list and type(expected_status) != set:
        expected_status = [ expected_status ]

      if response.status_code not in expected_status:
        raise StatusCodeException("Status code mismatch expected %s but got %s" % (expected_status, response.status_code))

    if response.status_code == 200:
      if expect_json:
        self._value = self.response["node"]["value"]
      # do well
    elif response.status_code  == 404:
        self._value = None
      # don't do well

  @property
  def value(self):
    return self._value

  def __repr__(self):
    return "<EtcdResponse %s, %s>" % (self.response, self.value)

class AsyncEtcdResponse(object):
  def __init__(self, deferred, expected_status, expect_json=True):
    self.deferred = deferred
    self.expected_status = expected_status
    self.expect_json = expect_json

    self.deferred.link_value(self._success)
    self.deferred.link_exception(self._failure)

    self.success_handlers =  []

    self.done = False
    self.failed = False

  def get(self, timeout=None):
    if self.done:
      return self.result
    elif self.failed:
      raise self.exception
    else:
      self.deferred.get(timeout=0.5)
      return self.response

  def success(self, handler):
    self.success_handlers.append(handler)

  def _process(self, response):
    return EtcdResponse(response, self.expected_status, self.expect_json)

  def _success(self, value):
    self.response = self._process(value.get())
    self.done = True

  def _failure(self, value):
    self.exception = Exception
    self.failed = True

  def __repr__(self):
    return "<AsyncResult at %s>" % (self.deferred)
