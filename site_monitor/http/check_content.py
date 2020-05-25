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
import re
import typing

import requests
from logzero import logger


def check_url_content(
    url: str, content_match: typing.Optional[re.Pattern] = None
) -> typing.Tuple[str, int, float, bool, datetime.datetime]:
    """
    Get URL and return basic information.

    Args:
        url (str): The URL to check.
        content_match (str): A regular expression to match on the content.


    Returns:
        A dict containing the information.
    """
    r = requests.get(url)
    content_found = False

    # If no content_match given, content_found should always be True.
    if content_match is None or content_match.search(r.text):
        content_found = True

    logger.debug(f"Finished querying {url}")

    return (
        url,
        r.status_code,
        r.elapsed.total_seconds(),
        content_found,
        datetime.datetime.now(datetime.timezone.utc),
    )
