import docker

from keep.actors import Actor

KEEP_STATS_KEY = "keep-service-stats"

class DockerStatsActor(Actor):

  def __init__(self, crow, polar_client, context):
    super(DockerStatsActor, self).__init__(context)

    self.crow = crow

    self.polar_client = polar_client
    self.docker_client = docker.Client(base_url='unix://var/run/docker.sock',
      version='1.13',
      timeout=10)

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
    stats_location_key = "%s/%s" % (KEEP_STATS_KEY, self.crow.hostname)

    node, stats = self.polar_client.get(stats_location_key)

    if not node:
      node, stats = self.polar_client.get(stats_location_key)

    current_containers = self.docker_client.containers()

    self.polar_client.set("%s/%s" % (stats_location_key, "container_count"), len(current_containers))

  def _update_services(self):
    pass
