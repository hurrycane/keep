from twitter.common import app

app.add_option('--with-ui', action="store_true", dest='with_ui',
               default=False, help="Enable UI for this node")

app.add_option('--ui-bind', dest='ui_bind', default="0.0.0.0",
               help="IP on which we bind the UI HTTP server")

app.add_option('--ui-port', dest='ui_port', default=8080,
               help="The port on which the UI starts.")

app.add_option('--etcd-host', dest='etcd_host', default="localhost",
               help="Host for one of the etcd peers in the cluster")

app.add_option('--etcd-port', dest='etcd_port', default=4001,
               help="Port for the etcd host")

app.add_option('--discovery', dest='discovery', default=None,
               help="Token used for the discovery service")

class Agent(object):

  def __init__(self, args):
    self.args = args

def main(args):
  args = app.get_options()

  if args.with_ui:
    HttpUI(
      host=args.ui_bind,
      port=ui_port
    )

  if args.discovery:
    etcd_handler = EtcdDiscovery(args.discovery)
  else:
    etcd_handler = EtcdPeer(host=args.etcd_host, port=args.etcd_port)

  crow = Crow(etcd=etcd_handler)

  Agent(crow).start()

app.main()
