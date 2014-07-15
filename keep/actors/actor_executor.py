from gevent.pool import Pool

from .actor_ref import ActorRef

_STOP = object()

class ActorExecutor(object):

  def __init__(self, actor_messaging, max_pool_size=100):
    self._actor_messaging = actor_messaging
    self.pool = Pool(max_pool_size)

  def spawn(self, actor_class, context):
    kwargs = actor_class._props
    kwargs["context"] = context

    actor_object = actor_class(**kwargs)

    if hasattr(actor_object, "on_start"):
      actor_object.on_start()

    greenlet = self.pool.spawn(self._actor_handler, actor_object)

    context.greenlet = greenlet

    return actor_object

  def join(self):
    return self.pool.join()

  def _actor_handler(self, actor):
    while True:
      item = actor.queue.get()

      if item["kind"] == "response":
        self._actor_messaging._asking_queues[ item["response-id"] ].put(
          item["body"]
        )

      if item == _STOP:
        break

      response = actor.on_receive(item["body"])

      if item["kind"] == "ask":

        response_actor_ref = actor.context.actor_selection(item["from"])
        for actor_ref in response_actor_ref:
          actor_ref._respond(response, item["ask-id"])
