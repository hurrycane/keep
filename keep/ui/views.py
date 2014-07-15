from flask import render_template, current_app
from flask import jsonify

from keep.ui import app

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/1.0/hosts')
def get_hosts():
  actor_system = current_app.config["actor_flask"]
  actor_ref = actor_system.actor_selection("/KeepRpcActor/HostsActor")

  try:
    hosts = actor_ref.ask({}, block=False, timeout=3)

    return jsonify(hosts)
  except:
    return jsonify(set([]))
