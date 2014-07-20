from keep.actors import Actor

from keep.agent.actors import HostsActor

class KeepRpcActor(Actor):

  def __init__(self, crow, context):
    super(KeepRpcActor, self).__init__(context)

    context.actor_of(HostsActor.props(crow=crow))

  def on_receive(self, message):
    #actor_ref = self.actor_selection("/KeepRpcActor")
    #actor_ref.tell("Trol!")
    # waits for the answer
    #future = actor_ref.ask("Trol!", block=False)
    print "Message from inside actor %s" % message
