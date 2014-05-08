python_library(
  name = 'keep_library',
  sources = globs('*.py') + globs('agent/*.py') + globs('actors/*.py'),
  dependencies = [
    python_requirement("twitter.common.app>=0.3.0"),
    python_requirement("pinject>=0.10.2")
  ]
)

python_binary(
  name = 'keep_agent',
  source = "agent/runner.py",
  dependencies = [
    pants(':keep_library'),
  ],
)
