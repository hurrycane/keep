from functools import partial

import requests

from keep.polar.protocol import Request


class Watcher(object):

  def __init__(self, client, path, request, watch_func, is_dir):
    self.client = client

    self.request = request
    self.watch_func = watch_func

    wait_index = None

    if is_dir:
      _, stats = self.client.set(path + "/_last_modified_index", -1)
      wait_index = stats["node"]["modifiedIndex"]

    result = self.client.handler.async_result()
    result.parser = None

    self.client.handler.callback_queue.put((
      partial(self.start, wait_index), result
    ))

  def start(self, wait_index=None):
    query_string = (self.request.query if self.request.query else []) + [ "wait=true" ]

    if wait_index != None:
      query_string += [ "waitIndex=%s" % (wait_index+1) ]

    # prepare the request with the wait_index

    request = Request(
      self.request.method,
      self.request.url,
      query_string,
      self.request.data
    )

    prepared = self.client._prepare(request)

    try:
      # do the request and wait for 0.2 seconds
      result = prepared(timeout=10)

      # if we're on this part of the try method it means that the etcd request
      # passed and not timed-out which means we need to call the callback

      # get the default parser for the handler
      parser = self.client.handler.async_result().parser
      value, stats = parser.parse(result)

      wait_index = stats["node"]["modifiedIndex"]

      self.client.handler.completion_queue.put((
        lambda: self.watch_func((value, stats)),
        self.client.handler.async_result()
      ))

    except requests.exceptions.Timeout:
      # if it fails via timeout do it again with the same wait_index
      pass
    finally:
      self.client.handler.callback_queue.put((
        partial(self.start, wait_index),
        self.client.handler.async_result()
      ))
