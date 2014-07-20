import gevent

from keep.actors import Actor

from keep.agent.actors import HostsActor, DockerActor

class KeepRpcActor(Actor):

  def __init__(self, crow, context):
    super(KeepRpcActor, self).__init__(context)

    context.actor_of(HostsActor.props(crow=crow))
    actor_ref = context.actor_of(DockerActor.props(crow=crow))

    gevent.spawn(self._periodically_update_docker_state, actor_ref)

  def on_receive(self, message):
    #actor_ref = self.actor_selection("/KeepRpcActor")
    #actor_ref.tell("Trol!")
    # waits for the answer
    #future = actor_ref.ask("Trol!", block=False)
    print "Message from inside actor %s" % message

  def _periodically_update_docker_state(self, actor_ref):
    while True:
      actor_ref.tell({ "message_type" : "updateState" })

      gevent.sleep(5)
