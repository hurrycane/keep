from keep.actors import Actor

class DockerExecutorActor(Actor):

  def __init__(self, crow, polar_client, context):
    super(DockerExecutorActor, self).__init__(context)

    self.crow = crow

  def on_receive(self, message):
    # needs to update the status in etcd periodically
    return "OK"
