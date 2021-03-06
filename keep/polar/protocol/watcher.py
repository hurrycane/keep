from functools import partial

import requests
import gevent

from gevent import socket

from keep.polar.protocol import Request
from keep.polar.exceptions import StaleData

import time


class Watcher(object):

  def __init__(self, client, path, request, watch_func, wait_index=None, is_dir=False):
    self.client = client
    self.handler = client.handler

    self.is_dir = is_dir
    self._path = path

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
    s = time.time()

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

    prepared = self.client._prepare(request)

    try:
      # do the request and wait for 0.2 seconds
      result = prepared(timeout=10)

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
    except gevent.Timeout:
      print "Timed out!"
    except socket.timeout:
      pass
    except StaleData:
      print "StaleData received"
      _, stats = self.client.get(self._path)
      wait_index = int(stats["stats"]["X-Etcd-Index"])
    finally:
      result = self.handler.async_result()

      self.client.handler.callback_queue.put((
        partial(self.start, wait_index),
        self.handler.async_result()
      ))
