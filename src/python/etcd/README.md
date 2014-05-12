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
  { "host": "http://host1", "port": 4001 },
  { "host": "http://host2", "port": 4001 },
])
```

With the [Discovery
token](http://coreos.com/docs/cluster-management/setup/etcd-cluster-discovery/)

```python

client = etcd.Client(discovery="https://discovery.etcd.io/17ca38d37aabbe650c3532db5fb1dbc9")
```

You can also make the library show the actual HTTP calls that makes to the
*etcd* cluster by passing ```debug=True``` to etcd.Client.

### Setting the value of a key

Having a client created as above, we can use it to write a key to the cluster.

```python
client.set("message", "value")
```

You can access the full response by passing the *Full* params to any of the
method calls.

```python

response = client.set("message", "Hello World", full=True)

response # => { "createdIndex": 2, "modifiedIndex": 2, "key": "/message",
"value" : "Hello World" }
```

### Getting a value of a key

The *Full* keyword is available too.

```python
value = client.get("message")
```
