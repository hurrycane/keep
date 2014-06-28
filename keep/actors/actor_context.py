class ActorContext(object):
  """
  Responsible for the context of a single actor
  """
  system = None

  def __init__(self, ref, actor_system):
    self._ref = ref
    self._parent  = ref.parent_ref
    self._system = actor_system
    self._actor = None

  @property
  def parent(self):
    return self._parent

  @property
  def actor(self):
    return self._actor

  @actor.setter
  def actor(self, value):
    self._actor = value

  @property
  def ref(self):
    return self._ref

  def actor_of(self, actor_class):
    # TODO: Make spawn actor public
    return self.system._spawn_actor(self, actor_class)
