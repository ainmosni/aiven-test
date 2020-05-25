# -*- coding: UTF-8 -*-
"""
Copyright 2020 Daniël Franke

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import typing

import click
import kafka.errors
import psycopg2
from logzero import logger

import site_monitor.kafka.consumer as kconsumer
import site_monitor.postgres.eventwriter as eventwriter

# Default kafka topic to send our events to.
DEFAULT_KAFKA_TOPIC = "site-monitor"


@click.command()
@click.option(
    "--kafka-bootstrap-server",
    "bootstrap_servers",
    multiple=True,
    default=["localhost",],
    help="Kafka bootstrap servers to use.",
)
@click.option(
    "--kafka-ca-file",
    "kafka_ca",
    type=str,
    required=True,
    help="Path to CA that signed the Kafka certifcates.",
)
@click.option(
    "--kafka-certificate-file",
    "kafka_cert",
    type=str,
    required=True,
    help="Path to certificate to authenticate with Kafka.",
)
@click.option(
    "--kafka-key-file",
    "kafka_key",
    type=str,
    required=True,
    help="Path to key for the Kafka certificate.",
)
@click.option(
    "-t",
    "--kafka-topic",
    "kafka_topic",
    type=str,
    default=DEFAULT_KAFKA_TOPIC,
    help="Kafka topic to send results to.",
)
@click.option(
    "--postgres-server",
    "postgres_server",
    type=str,
    required=True,
    help="Postgres instance to connect to.",
)
@click.option(
    "--postgres-port",
    "postgres_port",
    type=int,
    required=True,
    help="Port of the Postgres instance to connect to.",
)
@click.option(
    "--postgres-username",
    "postgres_user",
    type=str,
    required=True,
    help="Postgres username.",
)
@click.option(
    "--postgres-password",
    "postgres_password",
    type=str,
    required=True,
    help="Postgres password.",
)
@click.option(
    "--postgres-database",
    "postgres_database",
    type=str,
    required=True,
    help="Postgres database to use.",
)
def archive_events(
    bootstrap_servers: typing.List[str],
    kafka_ca: str,
    kafka_cert: str,
    kafka_key: str,
    kafka_topic: str,
    postgres_server: str,
    postgres_port: int,
    postgres_user: str,
    postgres_password: str,
    postgres_database: str,
):
    """
    Subsribes to a kafka topic for events and archives them to postgres.

    Args:
        bootstrap_servers (List[str]): Kafka bootstrap servers to connect to.
        kafka_ca (str): CA for Kafka certificates.
        kafka_cert (str): Kafka auth certificate.
        kafka_key (str): Kafka cert key.
        kafka_topic (str): Kafka topic to write events to.
        postgres_server (str): Postgres hostname.
        postgres_port (int): Postgres port.
        postgres_user: (str): Postgres user.
        postgres_password (str): Postgres password.
        postgres_database: (str): Postgres database.
    """
    try:
        writer = eventwriter.EventWriter(
            postgres_server,
            postgres_port,
            postgres_user,
            postgres_password,
            postgres_database,
        )
    except psycopg2.Error as e:
        logger.exception(e)
        sys, exit(1)

    try:
        for (
            url,
            status_code,
            response_time,
            content_found,
            timestamp,
        ) in kconsumer.get_events(
            bootstrap_servers, kafka_topic, kafka_ca, kafka_cert, kafka_key
        ):
            writer.write_event(
                url, status_code, response_time, content_found, timestamp
            )
    except kafka.errors.KafkaError as e:
        logger.exception(e)
        sys.exit(1)
