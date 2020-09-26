from typing import Any, Dict
from urllib.parse import urlparse

from {{cookiecutter.project_slug}}.config import config

__all__ = ("extract_database_credentials",)


def extract_database_credentials() -> Dict[str, Any]:
    """Extract database credentials from the database URL.

    :return: database credentials
    :rtype: Dict[str, Any]
    """
    parsed_url = urlparse(config["database"]["url"])
    return {
        "host": parsed_url.hostname,
        "port": parsed_url.port or 3306,
        "user": parsed_url.username,
        "password": parsed_url.password,
        "database": parsed_url.path[1:],
    }
