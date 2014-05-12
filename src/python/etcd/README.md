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

### Directories

Besides keys etcd supports directories.

#### Creating directories

Creating directories also creates in-order keys.

```python
response = client.mkdir("queue", "Job1")
response
{
  "node":{
    "createdIndex": 6,
    "key": "/queue/6",
    "modifiedIndex": 6,
    "value": "Job1"
  }
}
```

Full is by default enabled for *mkdir*.
Also mkdir can be valled without value.

##### Directires, TTL and refreshing

Like keys directories can expire after some time
```python
response = client.mkdir("queue", "job1", ttl=30)
```

You can *refresh* a directory by using *refreshdir*:
```python
response = client.refresh_dir("queue", ttl=30)
```

#### Listing directories

```python
for item in client.listdir("queue"):
  print item
```

### Watching for a key

You can watch for changes for a key:

```python

for change in client.watch("queue", recursive=True):
  print change

### Atomic CAS (Compare and Swap) and CAD (Compare and Delete)

```python

client.set("foo", "bar")

# compare and swap for value
client.set("foo", "barez", if_value="bar")

```

It also supports:

* if_index
* if_exists

### Consistency

For all of the above methods you can supply a consistent=True param that
would make the client redirect to the master.

### Lock

```python
# tries to acquires a lock for 60s, by default the timeout is 5s
lock = client.lock("key", ttl=60)

# tries to acquire a lock for 60s, it waits 2s for the response
lock = client.lock("key", ttl=60, timeout=2)

# renew ttl (same as acquire)
lock = client.lock("key", ttl=60)

# renew ttl with a certain index
lock = client.lock("key", ttl=60, index=2)
```

### Leader Election
```python
# only one will succed. If not will block until is acquires the leadership
leader = client.loader("key", "value", ttl=60, timeout=10)
```

## Changes

## TODOs & Ideas

* give the constructor a consistent=True param so that you don't have to pass
it everytime you're making a call.
