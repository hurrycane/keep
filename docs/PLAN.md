Keep Service
===========

Features:
* Deploy docker containers on any host, group of hosts
* Deploy services
  e.g Deploy 3 containers with API container version == v1.234
* Have a clear overview on which machines are UP at a certain point in time.
* Maintain N instances of a service.

Distributed features:
* Highly available => as long as the etcd cluster is available.
* It can recover from a failure (how to detect failure?)

Why?
Current deployment is error-prone as it-s manual.

Deployment steps:
* Choose image + version
* Chose one of: single instances, service.
* A service can be configured:
  * number of instances
  * dispers: auto, manual
  * hooks: post deployment, per node post/pre deployment.
* Individual hosts: chose one.
* Deployment starts.
* Status updates for each node.
* What runs where.


Architecture:

Each node has an KeepAgent.

KeepAgent:
* reports to etcd his status.
* reports periodically which docker containers are running.
* can execute docker tasks.
* it HTTP based.
* implies some security.
* knows which nodes are alive and which not.
* can have an UI activated (openes up a port).
* can start/restart/stop a container.
* can block deployments
* nodes can have tags

==

### Side notes
Crow as a library: get events when something changes.
                   daemon: that reads a config file and acts accordingly.
