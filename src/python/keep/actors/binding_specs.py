import pinject
import etcd


class ActorEtcdBindingSpec(pinject.BindingSpec):
  def __init__(self, host, port, discovery):
    super(ActorEtcdBindingSpec, self).__init__()

    self._host = host
    self._port = port
    self._discovery = discovery

  def configure(self, bind):

    if self._discovery:
      bind('etcd_handler', to_instance=etcd.AsyncClient(discovery=self._discovery))
    else:
      bind('etcd_handler', to_instance=etcd.AsyncClient(host=self._host,
                                                        port=self._port))

class CrowHostnameBindingSpec(pinject.BindingSpec):
  def __init__(self, hostname, namespace):
    super(CrowHostnameBindingSpec, self).__init__()

    self._hostname = hostname
    self._namespace = namespace

  def configure(self, bind):
    bind('hostname', to_instance=self._hostname)
    bind('namespace', to_instance=self._namespace)
