from actors import ActorRef

class ActorContext(object):

  def __init__(self, etcd_handler):
    self.registry = {}

  def actor_of(self, actor):
    actor_ref = ActorRef(actor)
    self.registry[actor_ref] = True

    return actor_ref
