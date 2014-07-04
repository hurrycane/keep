from keep.actors import Actor

class KeepRpcActor(Actor):

  def __init__(self, context):
    super(KeepRpcActor, self).__init__(context)

  def on_receive(self, message):
    #actor_ref = self.actor_selection("/KeepRpcActor")
    #actor_ref.tell("Trol!")
    # waits for the answer
    #future = actor_ref.ask("Trol!", block=False)
    print "Message from inside actor %s" % message
