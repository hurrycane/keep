from actors import Actor

class KeepRpcActor(Actor):
  def __init__(self, crow_context):
    self._crow_context = crow_context

  def on_receive(self, message):
    pass
    #sender = self.get_sender()
