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

from setuptools import setup, find_packages

setup(
    name="site_monitor",
    version="0.1",
    py_modules=find_packages(),
    install_requires=[
        "Click",
        "kafka-python",
        "requests",
        "logzero",
        "lz4",
        "crc32c",
        "psycopg2-binary",
    ],
    entry_points="""
        [console_scripts]
        site_monitor=site_monitor.monitor:monitor_site
        site_archiver=site_monitor.archiver:archive_events
    """,
)
