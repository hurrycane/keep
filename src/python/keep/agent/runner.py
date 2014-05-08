from twitter.common import app, log
from twitter.common.log.options import LogOptions

import pinject

app.add_option('--with-ui', action="store_true", dest='with_ui',
               default=False, help="Enable UI for this node")

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

from keep.actors import ActorContext
from keep.agent import KeepRpcActor
#from crow import CrowContext

def main(args, options):
  injector = pinject.new_object_graph(
    binding_specs=[
    ]
  )

  context = injector.provide(ActorContext)

  # start actor
  main_actor_ref = context.actor_of(KeepRpcActor.props(mama="pere"))

  #crow = injector.provide(CrowContext)
  #crow.add_handler("member-join", lambda member: main_actor_ref.tell(member))
  #crow.add_handler("member-leave", lambda member: main_actor_ref.tell(member))

  #crow.anounce()

# no GLOG to disk at least for now
LogOptions.set_disk_log_level('NONE')
# Log to stderr in GLOG format with minimum level DEBUG.
LogOptions.set_stderr_log_level('google:DEBUG')

app.main()
