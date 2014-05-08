Current Architecture

A Keep agent running on each machine. One of the keep agents can have an UI
enabled.

Sending messages to the UI to the keep agents is done via a HTTP API.

The concept of job is necessary:

- each operation that needs to be executed on a machine needs to be stored
  somewhere persistent. And is modeled as job.
- an keep agent has it s own Etcd-based Queue - from which it consumes jobs.

API:

GET /nodes # => get available nodes.
GET /nodes/<name>/running # => get the running containers
GET /nodes/<name>/running/<id> # => get info about a running container
POST /nodes/<name>/running # => start a new container
DELETE /nodes/<name>/running # => stop a new container

GET /deploy # lists on-going and finished deployments.
POST /deploy # creates a new deployment - custom logic for deployment is hardcoded.

GET /containers # get images with the latest versions
GET /pipelines # list deployment strategies
POST /pipelines # create a new deployment strategy
PUT /pipelines/<id> # update
DELETE /pipelines/<id> # delete

# non-MVP endpoints
GET /nodes/groups # lists the group of nodes
POST /nodes/groups # creates a group of nodes

##

State machine for keep

-> announces
-> updates list of nodes.

-> has it s own queue. Checks last index and starts consuming if there are jobs in the queue.
Periodically it writes his status in etcd with TTL.
