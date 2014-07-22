import json
import uuid
import time

from flask import render_template, current_app
from flask import jsonify, request

from keep.ui import app

INVALID = 403

KEEP_SERVICES = "keep-services"

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/1.0/hosts')
def get_hosts():
  actor_system = current_app.config["actor_flask"]
  actor_ref = actor_system.actor_selection("/KeepRpcActor/HostsActor")

  try:
    hosts = actor_ref[0].ask({}, block=False, timeout=3)

    return jsonify({ "hosts" : hosts})
  except:
    return jsonify(set([]))

@app.route('/1.0/available-images')
def get_available_image():
  return jsonify({
    "services" : [
      "2oteam/services-andromeda-api",
      "2oteam/services-game-server"
    ]
  })

@app.route('/1.0/service-versions')
def get_service_versions():
  service_name = request.args.get('service')
  polar_client = current_app.config["polar_client"]

  node, stats = polar_client.get("/services/%s" % service_name)

  large_version, small_version = node.split(".")

  return jsonify({
    "versions": [ "%s.%s" % (large_version, int(small_version) - i) for i in range(10) ]
  })

@app.route('/1.0/services', methods=["POST"])
def create_service():
  data = json.loads(request.data)
  data["updated_at"] = int(time.time())
  data["id"] = str(uuid.uuid4())

  polar_client = current_app.config["polar_client"]

  node, stats = polar_client.get(KEEP_SERVICES)
  if not node:
    polar_client.mkdir(KEEP_SERVICES)

  service_key = "%s/%s" % (KEEP_SERVICES, data["id"])
  polar_client.set(service_key, json.dumps(data))

  return "OK", 201


@app.route('/1.0/services')
def index_service():
  polar_client = current_app.config["polar_client"]

  node, stats = polar_client.get_children(KEEP_SERVICES)

  return jsonify({
    "services": [ json.loads(item["value"]) for item in node ]
  })

@app.route('/1.0/services', methods=["DELETE"])
def delete_service():
  polar_client = current_app.config["polar_client"]

  service_id = request.args.get('id')
  polar_client.delete("%s/%s" % (KEEP_SERVICES, service_id))

  return "OK"
