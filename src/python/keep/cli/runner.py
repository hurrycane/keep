from twitter.common import app, log
from twitter.common.log.options import LogOptions

import socket

import pinject
import gevent

app.add_option('--with-ui', action="store_true", dest='with_ui',
               default=False, help="Enable UI for this node")

app.add_option('--name', dest='hostname', default=socket.gethostname(),
               help="Name of the node that is running")

app.add_option('--namespace', dest='namespace', default="prod",
               help="Name of the node that is running")

app.add_option('--ui-bind', dest='ui_bind', default="0.0.0.0",
               help="IP on which we bind the UI HTTP server")

app.add_option('--ui-port', dest='ui_port', default=8080,
               help="The port on which the UI starts.")

app.add_option('--etcd_host', dest='etcd_host', default="localhost",
               help="Host for one of the etcd peers in the cluster")

app.add_option('--etcd_port', dest='etcd_port', default=4001,
               help="Port for the etcd host")

app.add_option('--discovery', dest='discovery', default=None,
               help="Token used for the discovery service")

from actors import ActorContext
from crow import CrowContext

from keep.agent import KeepRpcActor

from keep.actors.binding_specs import *

def main(args, options):
  # lock a build
  # get latest version of a service
  # compute the next version of a service
  # finish build

  injector = pinject.new_object_graph(
    binding_specs=[
      ActorEtcdBindingSpec(options.etcd_host, options.etcd_port,
                           options.discovery),
      CrowHostnameBindingSpec(options.hostname, options.namespace)
    ]
  )

  actor_context = injector.provide(ActorContext)
  crow_context = injector.provide(CrowContext)

  # start actor
  main_actor_ref = actor_context.actor_of(KeepRpcActor.props(
    crow_context=crow_context
  ))

  crow_context.add_handler("member-join",
                           lambda member: main_actor_ref.tell(member))
  crow_context.add_handler("member-leave",
                           lambda member: main_actor_ref.tell(member))

  #crow.anounce()

  gevent.wait()

# no GLOG to disk at least for now
LogOptions.set_disk_log_level('NONE')
# Log to stderr in GLOG format with minimum level DEBUG.
LogOptions.set_stderr_log_level('google:DEBUG')

app.main()
