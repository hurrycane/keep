import ujson

NOT_FOUND = 100

class JSONParser(object):

  def __init__(self):
    pass

  def parse(self, value):

    if value == None:
      return None, None

    parsed_value = ujson.loads(value.text)

    parsed_value["stats"] = value.headers
    parsed_value["stats"]["status_code"] = value.status_code

    if "errorCode" in parsed_value:
      # when we're in an error situation
      error_code = parsed_value["errorCode"]

      if error_code == NOT_FOUND:
        return None, parsed_value

    else:
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
