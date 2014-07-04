client = PolarClient(hosts=[])

client.start()

sleep(2) # let him start

client.get("mama", watch=enable_this_watcher)

@zk.ChildrenWatch("/my/favorite/node")
def watch_children(children):
  print("Children are now: %s" % children)

*
