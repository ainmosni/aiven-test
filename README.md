# aiven-test

## Preface

This is my result for the Aiven homework I received on 2020-05-18. Regretfully I didn't have enough time to complete everything I wanted, I will go over the things I wanted to add but couldn't in a later section.

## Installation

I used `pipenv` to manage my dependencies, and used `click` and `setuptools` to create the executables.

To install and test do the following.
```
$ cd path/to/src
$ pipenv install --three
$ pipenv shell
$ pip install .
```

This creates the `site_monitor` and `site_archiver` executables, `site_monitor` monitors the site and writes the events to Kafka, and `site_archiver` monitors Kafka, and archives the events to Postgres.

Executing them is simple, all the configuration options are explained when they are given the `--help` parameter.

## Things I didn't have time for.

This is a list of all the things I was planning to do but didn't have time for.

* Go through the source and check for naming consistency.
* Add testing via `pytest`.
* Add CI via GitHub actions.
* Create a Docker container.
* Make the commands configurable via a configuration file next to the command options.
* Do better logging.
* Add prometheus metrics.
* Create a kubernetes deployment.
