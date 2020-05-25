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

import datetime
import typing
import json

import kafka
import kafka.errors

from logzero import logger


def get_events(
    bootstrap_servers: typing.List[str], topic: str, ca: str, cert: str, key: str,
) -> typing.Tuple[str, int, float, bool, datetime.datetime]:
    """
    Generator for events, monitors a kafka topic and yields events when they arrive.

    Args:
        bootstrap_servers (List[str]): a list of Kafka bootstrap servers.
        topic (str): the topic that the object will use.
        ca (str): Path to CA file for certificate verification.
        cert (str): Path to certificate for authentication.
        key (str): Path to keyfile for the certificate.

    Returns:
        A KafkaConsumer.
    """
    logger.info(f"consuming topic {topic} on {bootstrap_servers}")
    consumer = kafka.KafkaConsumer(
        topic,
        security_protocol="SSL",
        ssl_ciphers="ALL",
        ssl_cafile=ca,
        ssl_certfile=cert,
        ssl_keyfile=key,
        ssl_check_hostname=False,
        bootstrap_servers=bootstrap_servers,
    )

    for message in consumer:
        event = json.loads(message.value.decode("utf-8"))
        yield (
            event["url"],
            event["status_code"],
            event["response_time"],
            event["content_found"],
            datetime.datetime.fromisoformat(event["timestamp"]),
        )
