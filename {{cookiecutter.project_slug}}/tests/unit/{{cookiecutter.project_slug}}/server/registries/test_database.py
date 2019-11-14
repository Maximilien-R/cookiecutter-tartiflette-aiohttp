from unittest.mock import Mock, patch

import aiomysql
import pytest

from asynctest import CoroutineMock

from {{cookiecutter.project_slug}}.server.registries import database, register_database_pool


@pytest.mark.asyncio
async def test_register_database_pool():
    app_mock = {}

    pool_mock = Mock()
    pool_mock.close = Mock()
    pool_mock.wait_closed = CoroutineMock()

    config_mock = {
        "database": {
            "host": "host",
            "port": 0,
            "user": "user",
            "password": "password",
            "database": "{{cookiecutter.project_slug}}",
        }
    }

    with patch(
        "{{cookiecutter.project_slug}}.server.registries.database.aiomysql.create_pool",
        new_callable=CoroutineMock,
        return_value=pool_mock,
    ) as create_pool_mock:
        with patch.object(database, "config", config_mock):
            async for _ in register_database_pool(app_mock):
                pass

        assert app_mock["database_pool"] is pool_mock
        create_pool_mock.assert_awaited_once_with(
            host=config_mock["database"]["host"],
            port=config_mock["database"]["port"],
            user=config_mock["database"]["user"],
            password=config_mock["database"]["password"],
            db=config_mock["database"]["database"],
            cursorclass=aiomysql.DictCursor,
        )
        pool_mock.close.assert_called_once()
        pool_mock.wait_closed.assert_awaited_once()
