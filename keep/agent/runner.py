import socket

import click

import gevent
from gevent import monkey as curious_george
curious_george.patch_all()

from keep.polar.client import PolarClient
from keep.polar.handlers import GeventHandler

from keep.actors import ActorSystem
from keep.agent.keep_rpc_actor import KeepRpcActor

from keep.crow import CrowContext

def validate_peers(ctx, param, value):
  if value == None:
    raise click.BadParameter("You need to provide at least one peer")

  try:
    peers_list = value.split(",")

    if all([ len(peer.split(":")) == 2 for peer in peers_list ]):
      return peers_list
    else:
      raise ValueError("Not in the proper format")

  except (ValueError, AttributeError):
    raise click.BadParameter('Peers need to be comma separated and have a port specified. e.g. example.com:4001' )

@click.command()
@click.option('--hostname', default=socket.gethostname(), help='Hostname that is reported to the service discovery part')
@click.option('--cluster', default="prod", help="Name of the cluster from which the node is part of")
@click.option('--with-ui', is_flag=True, default=False, help="Enable UI")
@click.option('--peers', help="Etcd cluster addresses, split by comma", callback=validate_peers)
def execute_from_cli(hostname, cluster, with_ui, peers):

  polar_client = PolarClient(hosts=peers, handler=GeventHandler())
  polar_client.start()

  crow = CrowContext(polar_client, hostname, cluster)

  actor_system = ActorSystem(
    polar_client=polar_client,
    name="%s-%s" % (hostname, cluster)
  )

  actor_system.actor_of(KeepRpcActor)

  crow.announce()

  #actor_ref = actor_system.actor_selection("/KeepRpcActor")
  #actor_ref.tell("Hai salut")

  print "Reached end"

  gevent.sleep(1000)
