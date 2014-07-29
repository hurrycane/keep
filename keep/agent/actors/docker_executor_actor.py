import json

from keep.actors import Actor

KEEP_SERVICES = "keep-services"

class DockerExecutorActor(Actor):

  def __init__(self, crow, polar_client, context):
    super(DockerExecutorActor, self).__init__(context)

    self.crow = crow
    self.polar_client = polar_client

  def on_receive(self, message):
    if message["message_type"] == "deploy":
      self._deploy(message["service"], message["version"])

    return "OK"

  def _deploy(self, service_id, version):
    service_data, stats = self.polar_client.get("%s/%s" % \
                                                (KEEP_SERVICES, service_id))

    service_data = json.loads(service_data)

    # connect to every host and tell them to start the container
    for host in service_data["hosts"]:
      actor_ref = self.context.actor_selection("actor.etcd://%s/KeepRpcActor/DockerExecutorActor" % host["name"])

      actor_ref[0].tell({})
