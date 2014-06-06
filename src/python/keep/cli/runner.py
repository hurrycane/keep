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
  "fetch_etcd_keys"
]

app.add_option('--get-latest-tag', dest='get_latest_tag',
               default=False, help="Fetch latest tag for the given service name")

app.add_option('--current-version', dest='current_version',
               default=False, help="Pass the current version of the build")

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

def start_build(options, service_name):
  pass

def finish_build(options, service_name):
  pass

def fetch_etcd_keys(options, hostname):
  pass

def main(args, options):
  for command in SUPPORTED_COMMANDS:
    if hasattr(options, command) and getattr(options, command) != False:
      method = globals()[command]
      method(options, getattr(options, command))

# no GLOG to disk at least for now
LogOptions.set_disk_log_level('NONE')
# Log to stderr in GLOG format with minimum level DEBUG.
LogOptions.set_stderr_log_level('google:DEBUG')

app.main()
