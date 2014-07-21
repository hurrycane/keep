from keep.actors import Actor

class DockerStatsActor(Actor):

  def __init__(self, crow, polar_client, context):
    super(DockerStatsActor, self).__init__(context)

    self.crow = crow

  def on_receive(self, message):
    # needs to update the status in etcd periodically
    # needs to update container stats

    # number of containers
    # what containers with image name and version
    # started time etc.

    # if needs to go through each service and find out
    # which is deployed on his hostname and update the status there
    # started / stopped / not deployed

    if message["message_type"] == "updateState":
      self._update_current_state()
      self._update_services()

    return "OK"

  def _update_current_state(self):
    pass

  def _update_services(self):
    pass
