python_library(
  name = 'etcd_library',
  sources = globs('*.py'),
  dependencies = [
    python_requirement("requests>=2.2.1"),
    python_requirement("grequests>=0.2.0")
  ],
  provides = setup_py(
    name = 'py-etcd',
    version = "0.1.4",
    description = "Full fledged etcd-client for python. Batteries included"
  )
)
