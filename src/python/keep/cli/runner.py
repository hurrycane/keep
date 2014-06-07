from twitter.common import app, log
from twitter.common.log.options import LogOptions

import os
import socket

import etcd

DISCOVERY_TOKEN = "DISCOVERY_TOKEN"
ETCD_SEED = "ETCD_SEED"

SUPPORTED_COMMANDS = [
  "get_latest_tag",
  "start_build",
  "finish_build",
  "fetch_etcd_keys",
  "next_version"
]

app.add_option('--get-latest-tag', dest='get_latest_tag',
               default=False, help="Fetch latest tag for the given service name")

app.add_option('--current-version', dest='current_version',
               default=False, help="Pass the current version of the build")

app.add_option('--next-version', dest='next_version',
               default=False, help="Compute the next version")

# --start-build service-andromeda-api --current-version 1.129
app.add_option('--start-build', dest='start_build',
               default=False, help="Start a build for a gen service")

# --finish-build service-andromeda-api --current-version 1.129
app.add_option('--finish-build', dest='finish_build',
               default=False, help="Finish a build that is already in progress")

app.add_option('--fetch-etcd-keys', dest='fetch_etcd_keys',
               default=False, help="Fetches an archive with the required keys\
                                    to start an etcd cluster")

def get_etcd_client():
  if DISCOVERY_TOKEN in os.environ:
    return etcd.Client(discovery=os.environ[DISCOVERY_TOKEN])

  if ETCD_SEED in os.environ:
    return etcd.Client(peers=os.environ[ETCD_SEED].split(","))

  return etcd.Client(peers=["etcd1-us-east-1-aws.2o.com:4001"])

def get_latest_tag(options, service_name):
  etcd_client = get_etcd_client()
  print etcd_client.get("/services/%s" % service_name).value

def start_build(options, service_name):
  etcd_client = get_etcd_client()

  if etcd_client.get("/services/locks/%s" % service_name).value != None:
    raise ValueError("Lock already set")

  etcd_client.set("/services/locks/%s" % service_name, "Value", ttl=360)

def finish_build(options, service_name):
  etcd_client = get_etcd_client()

  if etcd_client.get("/services/locks/%s" % service_name).value != None:
    etcd_client.delete("/services/locks/%s" % service_name)

  if not hasattr(options, "current_version") or options.current_version == False:
    raise ValueError("Current version needs to be specified")

  current_version = options.current_version

  value = [ int(i) for i in current_version.split(".") ]

  if len(value) != 2:
    raise AttributeError("Version needs to have only two components")

  value[-1] += 1
  next_version = ".".join([ str(i) for i in value ])

  etcd_client.set("services/%s" % service_name, next_version)
  print etcd_client.get("services/%s" % service_name).value

def next_version(options, version):
  current_version = version

  value = [ int(i) for i in current_version.split(".") ]

  if len(value) != 2:
    raise AttributeError("Version needs to have only two components")

  value[-1] += 1
  next_version = ".".join([ str(i) for i in value ])

  print next_version


def fetch_etcd_keys(options, hostname):
  pass

def main(args, options):
  for command in SUPPORTED_COMMANDS:
    if hasattr(options, command) and getattr(options, command) != False:
      method = globals()[command]
      method(options, getattr(options, command))

# no GLOG to disk at least for now
#LogOptions.set_disk_log_level('NONE')
# Log to stderr in GLOG format with minimum level DEBUG.
LogOptions.set_stderr_log_level('google:ERROR')

app.main()
