class EtcdResponse(object):
  def __init__(self, response, expected_status):
    self.response = response

class AsyncEtcdResponse(object):
  def __init__(self, response, expected_status):
    self.response = response
