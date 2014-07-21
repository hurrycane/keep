import gevent

from keep.actors import Actor

from keep.agent.actors import HostsActor, DockerStatsActor, DockerExecutorActor

class KeepRpcActor(Actor):

  def __init__(self, crow, polar_client, context):
    super(KeepRpcActor, self).__init__(context)

    context.actor_of(HostsActor.props(crow=crow))

    stats_actor_ref = context.actor_of(
      DockerStatsActor.props(crow=crow, polar_client=polar_client)
    )

    docker_actor_ref = context.actor_of(
      DockerExecutorActor.props(crow=crow, polar_client=polar_client)
    )

    gevent.spawn(
      self._periodically_send_message,
      stats_actor_ref,
      { "message_type" : "updateState" },
      5
    )

    gevent.spawn(
      self._periodically_send_message,
      docker_actor_ref,
      { "message_type" : "checkState" },
      10
    )

  def on_receive(self, message):
    print "Message from inside KeepRPCActor %s" % message
    return "OK"

  def _periodically_send_message(self, actor_ref, message, sleep_timeout):
    while True:
      actor_ref.tell(message)
      gevent.sleep(sleep_timeout)
