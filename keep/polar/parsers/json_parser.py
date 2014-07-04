from __future__ import print_function

import ujson
import sys

from keep.polar.exceptions import StaleData

NOT_FOUND = 100
TEST_FAILED = 101
NOT_A_FILE = 102
NOT_A_DIRECTORY = 104

EVENT_INDEX_CLEARED = 401

def warning(*objs):
  print("WARNING: ", *objs, file=sys.stderr)

class JSONParser(object):

  def __init__(self):
    pass

  def parse(self, value):

    if value == None:
      return None, None

    parsed_value = ujson.loads(value.text)

    warning(parsed_value)

    parsed_value["stats"] = value.headers
    parsed_value["stats"]["status_code"] = value.status_code

    if "errorCode" in parsed_value:
      # when we're in an error situation
      error_code = parsed_value["errorCode"]

      if error_code == NOT_FOUND:
        return None, parsed_value

      if error_code == TEST_FAILED:
        return None, parsed_value

      if error_code == NOT_A_FILE:
        return None, parsed_value

      if error_code == EVENT_INDEX_CLEARED:
        raise StaleData(parsed_value)

      if error_code == NOT_A_DIRECTORY:
        return None, parsed_value

    else:
      if parsed_value["action"] == "expire":
        return None, parsed_value

      if "dir" in parsed_value["node"]:
        value = []

        if "nodes" in parsed_value["node"]:
          value = parsed_value["node"]["nodes"]

        return value, parsed_value

      else:
        if parsed_value["action"] == "delete":
          return None, parsed_value

        return_value = parsed_value["node"]["value"]
        return return_value, parsed_value
