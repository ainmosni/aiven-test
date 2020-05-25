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

import json
import typing
import datetime

import kafka
import kafka.errors

from logzero import logger


class EventProducer:
    """
    This is small wrapper around the KafkaProducer, to make sending events easier
    and less error prone.
    """

    def __init__(
        self,
        bootstrap_servers: typing.List[str],
        topic: str,
        ca: str,
        cert: str,
        key: str,
    ) -> kafka.KafkaProducer:
        """
        Creates and returns a KafkaProducer, configured to serialise messages as json.

        Args:
            bootstrap_servers (List[str]): a list of Kafka bootstrap servers.
            topic (str): The topic to write to.
            ca (str): Path to CA file for certificate verification.
            cert (str): Path to certificate for authentication.
            key (str): Path to keyfile for the certificate.

        Returns:
            A KafkaProducer.
        """
        logger.info(f"connecting producer to {bootstrap_servers}")
        self.producer = kafka.KafkaProducer(
            security_protocol="SSL",
            ssl_ciphers="ALL",
            ssl_cafile=ca,
            ssl_certfile=cert,
            ssl_keyfile=key,
            ssl_check_hostname=False,
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda m: json.dumps(m).encode("utf-8"),
        )
        logger.debug("Connected to Kafka")
        self.topic = topic

    def write_event(
        self,
        url: str,
        status_code: int,
        response_time: float,
        content_found: bool,
        timestamp: datetime.datetime,
    ):
        """
        Serialises and writes an event to the kafka topic.

        Args:
            url (str): URL queried.
            status_code (int): The status code of the event.
            response_time (float): The response time of the server.
            content_found (bool): If the expected content was found.
            timestamp (datetime): The timestamp of the event.
        """
        message = {
            "url": url,
            "status_code": status_code,
            "response_time": response_time,
            "content_found": content_found,
            "timestamp": timestamp.isoformat(),
        }
        self.producer.send(self.topic, message)
        logger.debug(f"Written message to {self.topic}")
