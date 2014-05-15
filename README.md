keep
====

Continuos integration and deployment service build open service discovery service crow.

Uses [Pants](http://pantsbuild.github.io/) and [PEX](https://www.youtube.com/watch?v=NmpnGhRwsu0) for building and distributing.

# Building Keep

Checkout the Keep

```
git clone git@github.com:hurrycane/keep.git
```

Create a virtualenv and install:

```
pip install twitter.pants
```

To actually build the PEX file for the keep agent run:

```
pants src/python/keep:keep_agent
```

For running tests:

```
pants tests/python
```

## Powered by:

* twitter.pants
* twitter.common.app
* requests / grequests
* gevent
