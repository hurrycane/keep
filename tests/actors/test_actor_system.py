import gevent
import pytest

from keep.actors import ActorSystem, Actor

class SimpleActor(Actor):
  def __init__(self, context):
    super(SimpleActor, self).__init__(context)

  def on_receive(self, message):
    print "SimpleActor says %s" % message
    return "OK"

def test_actor_system_init():
  with ActorSystem(None, "testing-test") as actor_system:
    actor_system.actor_of(SimpleActor)

def test_actor_system_selection():
  class TestActor(Actor):

    def __init__(self, context):
      super(TestActor, self).__init__(context)

    def on_start(self):
      actor_ref = self.context.actor_of(SimpleActor)
      actor_ref = self.context.actor_of(SimpleActor)

      assert len(self.context.actor_selection("SimpleActor")) == 2

    def on_receive(self, message):
      return "OK"

  with ActorSystem(None, "testing-test") as actor_system:
    actor_ref = actor_system.actor_of(TestActor)

    assert len(actor_system.actor_selection("*")) == 1
    assert len(actor_system.actor_selection("TestActor/SimpleActor")) == 2

def test_actor_communication():
  class VerySimpleActor(Actor):
    count = 0

    def __init__(self, context):
      super(VerySimpleActor, self).__init__(context)

    def on_receive(self, message):
      VerySimpleActor.count += 1
      return "OK"

  with ActorSystem(None, "testing-test") as actor_system:
    actor_ref = actor_system.actor_of(VerySimpleActor)
    actor_ref.tell({})

    gevent.sleep(1)

    assert VerySimpleActor.count == 1

def test_actor_system_init_props():
  class MadSimpleActor(Actor):

    def __init__(self, context, atom):
      super(MadSimpleActor, self).__init__(context)

    def on_receive(self, message):
      return "OK"

  with ActorSystem(None, "testing-test") as actor_system:
    actor_system.actor_of(MadSimpleActor.props(atom=1))

def test_actor_system_ask():
  class TalkSimpleActor(Actor):

    def __init__(self, context):
      super(TalkSimpleActor, self).__init__(context)

    def on_receive(self, message):
      print message
      return "OK"

  with ActorSystem(None, "testing-test") as actor_system:
    actor_ref = actor_system.actor_of(TalkSimpleActor)

    response = actor_ref.ask("Hai salut!")
    assert response  == "OK"
