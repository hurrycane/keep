# py-etcd API

## Basic Operations

The primary API for etcd is a [hierarchical key space](https://github.com/coreos/etcd/blob/master/Documentation/api.md#key-space-operations). _Keys_ can be either directories or keys (nodes).

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
_etcd_ cluster by passing ```debug=True``` to etcd.Client.

### Setting the value of a key

Having a client created as above, we can use it to write a key to the cluster.

```python
client.set("message", "value")
```

You can access the full response by passing the _Full_ params to any of the
method calls.

```python

response = client.set("message", "Hello World", full=True)

response
{
   "node":{
      "createdIndex":2,
      "modifiedIndex":2,
      "key":"/message",
      "value":"Hello World"
   }
}
```

### Getting a value of a key

The _Full_ keyword is available too.

```python
value = client.get("message")
```

It returns None is the key was not found.

### Deleting a key

```python

response = client.delete("message", full=True)
```

### Using key TTL

Keys in *etcd* can expire after a specified number of seconds.

```python
client.set("message", "value", ttl=5)

```

After 5 seconds the key will be deleted and None will be returned if you
call get for the same key.

#### Refresh a key

A key TTL can be refreshed

```python
client.refresh("key", ttl=5)
```

Also A key TTL can be deleted

```python
client.refresh("key", ttl=False)
```

### Creating a directory

Directory + TTL + Listing + Deleting

### Watching for a key

### Atomic CAS (Compare and Swap) and CAD (Compare and Delete)

### Consistency

consistent=true

### Lock

### Leader Election

## Changes

## TODOs & Ideas

* give the constructor a consistent=True param so that you don't have to pass
it everytime you're making a call.
