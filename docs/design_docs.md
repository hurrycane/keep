Keep is a Cluster Scheduler built for docker.

Features:

* start / stop / restart containers / set ports / attach volumes
* service update (atomically)
* stage aware
* provides service discovery for containers (where is ZooKeeper located?)
  * via HTTP
* provides monitoring information about the container
* replicate / resize
* tag containers, integrates with the service discovery tool
* [Future] load balance containers
