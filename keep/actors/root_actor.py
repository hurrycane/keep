from keep.actors import Actor

class RootActor(Actor):

  def __init__(self, context):
    super(RootActor, self).__init__(context)

  def on_receive(self, message):
    print "Message from inside RootActor %s" % message
