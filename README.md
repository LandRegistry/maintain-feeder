# Maintain Feeder


## Unit tests

The unit tests are contained in the unit_tests folder. [Pytest](http://docs.pytest.org/en/latest/) is used for unit testing. 

To run the unit tests if you are using the common dev-env use the following command:

```bash
docker-compose exec maintain-feeder make unittest
or, using the alias
unit-test maintain-feeder
```

or

```bash
docker-compose exec maintain-feeder make report="true" unittest
or, using the alias
unit-test maintain-feeder -r
```

# Linting

Linting is performed with [Flake8](http://flake8.pycqa.org/en/latest/). To run linting:
```bash
docker-compose exec maintain-feeder make lint
```

# Naming

For reasons of compliance, the actual name of this module is maintain-feeder-client, the "actual_name" file will cause the RPM to built with this name and it's also the name the service will run under and the folder it will be in when deployed to a server.
