python_tests(name = 'etcd_tests',
  dependencies = [
    pants('src/python/etcd/BUILD:etcd_library'),
    python_requirement("mock>=1.0.1"),
    python_requirement("PyHamcrest>=1.8.0")
  ],
  sources = globs('*.py'),
  coverage = 'etcd'
)
