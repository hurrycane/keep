import uuid

from gevent.queue import Empty

class ActorRef(object):

  def __init__(self, from_context, absolute_path):
    self._from_context = from_context
    self._actor_messaging = from_context._messaging

    self._absolute_path = absolute_path

  def tell(self, message_body):
    message = self._build_message(message_body)
    message["kind"] = "tell"

    self._from_context._messaging.tell(self._absolute_path, message)

  def ask(self, message_body, block=True, timeout=-1):
    message = self._build_message(message_body)
    message["kind"] = "ask"
    message["ask-id"] = str(uuid.uuid4())

    self._from_context._messaging.ask(self._absolute_path, message)

    while True:
      try:
        return self._actor_messaging._asking_queues[ message["ask-id"] ].get(timeout=10)
      except Empty:
        pass

  def _respond(self, message_body, response_id):
    message = self._build_message(message_body)
    message["kind"] = "response"
    message["response-id"] = response_id

    self._from_context._messaging.tell(self._absolute_path, message)

  def _build_message(self, message_body):
    from_path = self._from_context._absolute_path
    from_path = "/" if from_path == "" else from_path

    return {
      "from": from_path,
      "to": self._absolute_path,
      "body": message_body
    }
