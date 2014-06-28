from functools import partial

import requests

from keep.polar.protocol import Request


class Watcher(object):

  def __init__(self, client, path, request, watch_func, wait_index=None, is_dir=False):
    self.client = client
    self.handler = client.handler

    self.is_dir = is_dir

    self.request = request
    self.watch_func = watch_func

    result = self.handler.async_result()
    result.parser = None

    if wait_index == None:
      _, stats = client.get(path)

      wait_index = int(stats["stats"]["X-Etcd-Index"])

    self.client.handler.callback_queue.put((
      partial(self.start, wait_index), result
    ))

  def start(self, wait_index=None):
    query_string = (
      self.request.query if self.request.query else []
    ) + [ "wait=true" ]

    if wait_index != None:
      query_string += [ "waitIndex=%s" % (wait_index+1) ]

    if self.is_dir:
      query_string += [ "recursive=true" ]

    request = Request(
      self.request.method,
      self.request.url,
      query_string,
      self.request.data
    )

    print "Watcher", request.method, request.url

    prepared = self.client._prepare(request)

    try:
      # do the request and wait for 0.2 seconds
      result = prepared(timeout=0.2)

      print "Event!"

      # if we're on this part of the try method it means that the etcd request
      # passed and not timed-out which means we need to call the callback

      # get the default parser for the handler
      parser = self.handler.async_result().parser
      # parse
      value, stats = parser.parse(result)

      # update wait_index
      wait_index = stats["node"]["modifiedIndex"]

      # spawn the callback
      self.handler.spawn(self.watch_func, (value, stats))

    except requests.exceptions.Timeout:
      # if it fails via timeout do it again with the same wait_index
      pass
    finally:
      result = self.handler.async_result()

      self.client.handler.callback_queue.put((
        partial(self.start, wait_index),
        self.handler.async_result()
      ))
