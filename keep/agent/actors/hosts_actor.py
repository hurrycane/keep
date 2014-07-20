from keep.actors import Actor

class HostsActor(Actor):

  def __init__(self, crow, context):
    super(HostsActor, self).__init__(context)

    self.crow = crow

  def on_receive(self, message):
    alive_hosts = self.crow.hosts
    known_hosts = self.crow.known_hosts

    return [ { "name" : host, "alive" : host in alive_hosts } for host in known_hosts ]
