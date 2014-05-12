# py-etcd API

## Basic Operations

### Creating the base client

With only a peer
```
import etcd

client = etcd.Client(host="http://localhost", port=4001)
```

With a list of peers:

``` python
client = etcd.Client(peers=[
  { host: "http://host1", port: 4001 },
  { host: "http://host2", port: 4001 },
])
```

With the [Discovery
token](http://coreos.com/docs/cluster-management/setup/etcd-cluster-discovery/)

```python

client
= etcd.Client(discovery="https://discovery.etcd.io/17ca38d37aabbe650c3532db5fb1dbc9")
```

### Setting the value of a key

```python

```
