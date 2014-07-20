from keep.actors import Actor

class DockerActor(Actor):

  def __init__(self, crow, context):
    super(DockerActor, self).__init__(context)

    self.crow = crow

  def on_receive(self, message):
    print message

    return "OK"
