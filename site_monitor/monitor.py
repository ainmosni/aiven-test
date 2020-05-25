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

import re
import typing
import time
import sys

import click
import kafka.errors
from logzero import logger

import site_monitor.kafka.producer as kproducer
import site_monitor.http as http

# Default interval to check the site in seconds.
DEFAULT_INTERVAL = 10

# Default kafka topic to send our events to.
DEFAULT_KAFKA_TOPIC = "site-monitor"


@click.command()
@click.option(
    "-i",
    "--interval",
    "interval",
    type=int,
    show_default=True,
    default=DEFAULT_INTERVAL,
    help="Period of time between checks, in seconds.",
)
@click.option(
    "-c",
    "--content-match",
    "content_match",
    type=str,
    default=None,
    help="Regular expression to match on the response content.",
)
@click.option(
    "-k",
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
@click.argument("url", type=str)
def monitor_site(
    interval: int,
    content_match: str,
    bootstrap_servers: typing.List[str],
    kafka_ca: str,
    kafka_cert: str,
    kafka_key: str,
    kafka_topic: str,
    url: str,
) -> None:
    """
    Monitors an URL, and pushes the data to a kafka topic.

    Args:
        interval (str): Monitoring interval.
        content_match (str): Regular expression to match the site content on.
        bootstrap_servers (List[str]): Kafka bootstrap servers to connect to.
        kafka_ca (str): CA that signed the Kafka certs.
        kafka_cert (str): Certificate to authenticate with Kafka.
        kafka_key (str): Key for the Kafka certificate.
        kafka_topic (str): Kafka topic to write events to.
        name (str): The url to monitor.
    """

    try:
        producer = kproducer.EventProducer(
            bootstrap_servers, DEFAULT_KAFKA_TOPIC, kafka_ca, kafka_cert, kafka_key,
        )
    except kafka.errors.KafkaError as e:
        logger.exception(e)
        sys.exit(1)
    logger.debug("Connected to Kafka")

    if content_match is not None:
        try:
            content_match = re.compile(content_match)
        except re.error as e:
            logger.exception(e)
            sys.exit(1)

    while True:
        (
            url,
            status_code,
            response_time,
            content_found,
            timestamp,
        ) = http.check_url_content(url, content_match)
        producer.write_event(url, status_code, response_time, content_found, timestamp)

        time.sleep(interval)
