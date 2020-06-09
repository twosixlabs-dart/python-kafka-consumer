# python-kafka-consumer

[![Build Status](https://github.com/twosixlabs-dart/python-kafka-consumer/workflows/Build/badge.svg)](https://github.com/twosixlabs-dart/python-kafka-consumer/actions)

## What Is This?

This project contains an example for working with Kafka Streams via the [`Faust`](https://faust.readthedocs.io) library. This particular project contains a simple read-only consumer implementation. The full suite of projects are the following:

- [Producer](https://github.com/twosixlabs-dart/python-kafka-producer)
- [Stream Processor](https://github.com/twosixlabs-dart/python-kafka-streams)
- [Consumer](https://github.com/twosixlabs-dart/python-kafka-consumer) (this project)
- [Environment](https://github.com/twosixlabs-dart/kafka-examples-docker)

The *consumer* in this example is an agent that subscribes to some topic using SSL/SASL to consume and record events. When it receives an event it dumps the payload to a file. That is it!

## Getting Started

Getting started with this example requires a complete Kafka environment. If you are getting started completely from nothing, [this project](https://github.com/twosixlabs-dart/kafka-examples-docker) contains a docker-compose file for setting up everything. Alternatively you can use the configuration inputs to connect to a preexisting infrastructure if one is already available.

### Configuration File & SASL/SSL

The code here is configured to use JSON resources found at the subpackage `pyconsumer.resources.env`. Your configuration must be found within the [pyconsumer/resources/env](pyconsumer/resources/env) directory.

The default is to point to the [wm-sasl-example](/pyconsumer/resources/env/wm-sasl-example.json) configuration (which contains mostly nothing). Feel free to edit this file for any runs you make. Here is the expected format of the input file:

```json
{
    "kafka.bootstrap.servers": "",
    "auth": {
        "username": "",
        "password": ""
    },
    "app": {
        "id": "",
        "auto_offset_reset": "",
        "enable_auto_commit": false
    },
    "topic": {
        "from": ""
    },
    "persist.dir": ""
}
```

* `kafka.bootstrap.servers` - the hostname + port of the Kafka broker
* `auth`
  * `username` - username for SASL authentication
  * `password` - password for SASL authentication
* `app`
  * `id` - unique identifier for your application/group
  * `auto_offset_reset` - set to either `earliest` or `latest` to determine where a *new* app should start consuming from
  * `enable_auto_commit` - set to true to commit completed processing records
* `topic`
  * `from` - topic to consume from; currently only a single topic may be specified
* `persist.dir` - unique to this example, this is used during processing for dumping received records to disk.

These options are subject to change/refinement, and others may be introduced in the future.

### Running the Application

You have the option of running the application directly on your machine or within a Docker container.

#### Directly

Install dependencies:

```shell
python -m pip install -r requirements.txt
```

Execute:

```shell
python -m pyconsumer worker -l info
```

This will begin generating a substantial amount of output, including a number of "warnings" that data is being persisted. These warnings are expected and good! The output will then halt, as the application is waiting for more data to be sent to the topic. You can observe the documents in the `persist.dir` that was specified.

#### Docker

Build the Docker image:

```shell
docker build -t python-kafka-consumer-local .
```

Execute:

```shell
mkdir /home/user/kafka_output
docker run --env PROGRAM_ARGS=wm-sasl-example -it -v /home/user/kafka_output:/opt/app/data python-kafka-consumer-local:latest
```

Here we are mapping a local directory `kafka_output` to the Docker directory that Kafka is configured to dump to. Note this should be an absolute path, otherwise Docker will not treat the volume properly. This will begin generating a substantial amount of output, including a number of "warnings" that data is being persisted. These warnings are expected and good! The output will then halt, as the application is waiting for more data to be sent to the topic. You can observe the documents in the `kafka_output` that was created locally on your machine.
