from unittest.mock import Mock, patch

import aiomysql
import pytest

from asynctest import CoroutineMock

from {{cookiecutter.project_slug}}.server.registries import register_database_pool


@pytest.mark.asyncio
async def test_register_database_pool():
    app_mock = {}

    pool_mock = Mock()
    pool_mock.close = Mock()
    pool_mock.wait_closed = CoroutineMock()

    database_credentials_mock = {
        "host": "host",
        "port": 0,
        "user": "user",
        "password": "password",
        "database": "my_app",
    }

    with patch(
        "{{cookiecutter.project_slug}}.server.registries.database.aiomysql.create_pool",
        new_callable=CoroutineMock,
        return_value=pool_mock,
    ) as create_pool_mock:
        with patch(
            "{{cookiecutter.project_slug}}.server.registries.database.extract_database_credentials",
            return_value=database_credentials_mock,
        ):
            async for _ in register_database_pool(app_mock):
                pass

        assert app_mock["database_pool"] is pool_mock
        create_pool_mock.assert_awaited_once_with(
            host=database_credentials_mock["host"],
            port=database_credentials_mock["port"],
            user=database_credentials_mock["user"],
            password=database_credentials_mock["password"],
            db=database_credentials_mock["database"],
            cursorclass=aiomysql.DictCursor,
        )
        pool_mock.close.assert_called_once()
        pool_mock.wait_closed.assert_awaited_once()
