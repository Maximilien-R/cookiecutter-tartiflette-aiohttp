import pytest

from unittest.mock import patch

from {{cookiecutter.project_slug}}.utils import (
    database,
    extract_database_credentials,
)


@pytest.mark.parametrize("database_url,expected", [
    (
        "mysql://user:password@database:3210/database_name",
        {
            "host": "database",
            "port": 3210,
            "user": "user",
            "password": "password",
            "database": "database_name",
        },
    ),
    (
        "mysql://user:password@database/database_name",
        {
            "host": "database",
            "port": 3306,
            "user": "user",
            "password": "password",
            "database": "database_name",
        },
    ),
])
def test_extract_database_credentials(database_url, expected):
    config_mock = {"database": {"url": database_url}}
    with patch.object(database, "config", config_mock):
        assert extract_database_credentials() == expected
