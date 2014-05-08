keep
====

Continuos integration and deployment service build open service discovery service crow.

Uses [Pants](http://pantsbuild.github.io/) and [PEX](https://www.youtube.com/watch?v=NmpnGhRwsu0) for building and distributing.

# Building Keep

Checkout the Keep

```
git clone git@github.com:hurrycane/keep.git
```

in the *keep* directory run:

```
./pants
```

this bootstraps the build tool.

To actually build the PEX file for the keep agent run:

```
./pants src/python/keep:keep_agent
```
