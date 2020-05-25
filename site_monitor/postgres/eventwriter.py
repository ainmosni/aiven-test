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

import psycopg2


class EventWriter:
    """
    Class to write events to postgres.
    """

    def __init__(
        self, host: str, port: int, user: str, password: str, database: str
    ) -> None:
        """
        Initialises the eventwrite and the database. Will connect to postgres,
        and initialise the table.

        Args:
            host (str): The pg host to connect to.
            port (str): The pg port to connect to.
            user (str): The user to use for authentication.
            password (str): The password to use for authentication.
            database (str): The database to connect to.
        """
        creds = {
            "dbname": database,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
            "sslmode": "require",
        }
        self.conn = psycopg2.connect(**creds)
        self.__initialise_table()

    def __initialise_table(self) -> None:
        """
        Initialises the table if it doesn't exist.
        """
        cur = self.conn.cursor()
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS "monitor_events" (
            id SERIAL PRIMARY KEY,
            URL text NOT NULL,
            status_code integer NOT NULL,
            response_time numeric NOT NULL,
            content_found boolean NOT NULL,
            timestamp timestamp with time zone NOT NULL
        )
        """
        )
        self.conn.commit()

    def write_event(
        self,
        url: str,
        status_code: int,
        response_time: float,
        content_found: bool,
        timestamp: datetime.datetime,
    ):
        """
        Writes an event to postgres.

        Args:
            url (str): The URL queried.
            status_code (int): The status code that was returned.
            response_time (float): The response time.
            content_found (bool): If the expected content was found.
            timestamp (datetime.datetime): The time of the request.
        """
        cur = self.conn.cursor()
        cur.execute(
            """
        INSERT INTO monitor_events
        (URL, status_code, response_time, content_found, timestamp)
        VALUES
        (%s, %s, %s, %s, %s)
        """,
            (url, status_code, response_time, content_found, timestamp),
        )
        self.conn.commit()
