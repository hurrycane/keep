class CrowContext(object):

  """
  CrowContext.
  """
  def __init__(self, etcd_handler):
    self.etcd = etcd_handler

  def add_handler(self, event, handler):
    pass
