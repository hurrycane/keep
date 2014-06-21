from setuptools import setup, find_packages

requires = []

setup(name="keep",
      version="0.0.1",
      platforms='any',
      packages = find_packages(),
      include_package_data=True,
      install_requires=requires,
      author = "Bogdan Gaza",
      author_email = "bc.gaza@gmail.com",
      url = "https://github.com/hurrycane/keep",
      description = """A distributed docker runner""",
      keywords = ['keep', 'docker', 'etcd', 'distributed'],
      entry_points = {'console_scripts': [ 'keep-agent = keep.agent.runner:execute_from_cli' ]},
      test_requirements = [],
      classifiers = [
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Topic :: Database :: Front-Ends",
      ]
)
