python_library(
  name = 'keep_library',
  sources = globs('*.py') + globs('agent/*.py') + globs('actors/*.py')  + globs('cli/*.py'),
  dependencies = [
    python_requirement("twitter.common.app>=0.3.0"),
    python_requirement("pinject>=0.10.2")
  ]
)

python_binary(
  name = 'keep_agent',
  source = "agent/runner.py",
  dependencies = [
    pants('src/python/actors/BUILD:actors_library'),
    pants('src/python/etcd/BUILD:etcd_library'),
    pants('src/python/crow/BUILD:crow_library'),
    pants(':keep_library'),
  ],
)

python_binary(
  name = 'keep-cli',
  source = "cli/runner.py",
  dependencies = [
    pants('src/python/actors/BUILD:actors_library'),
    pants('src/python/etcd/BUILD:etcd_library'),
    pants('src/python/crow/BUILD:crow_library'),
    pants(':keep_library'),
  ],
)
