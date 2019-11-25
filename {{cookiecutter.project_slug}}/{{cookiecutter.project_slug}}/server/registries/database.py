import aiomysql

from {{cookiecutter.project_slug}}.utils import extract_database_credentials

__all__ = ("register_database_pool",)


async def register_database_pool(app: "aiohttp.web.Application") -> None:
    """
    Creates a MySQL pool and register it into the application.
    :param app: application to which register the MySQL pool
    :type app: aiohttp.web.Application
    """
    # pylint: disable=missing-yield-doc
    database_credentials = extract_database_credentials()
    pool = await aiomysql.create_pool(
        host=database_credentials["host"],
        port=database_credentials["port"],
        user=database_credentials["user"],
        password=database_credentials["password"],
        db=database_credentials["database"],
        cursorclass=aiomysql.DictCursor,
    )
    app["database_pool"] = pool
    yield
    pool.close()
    await pool.wait_closed()
