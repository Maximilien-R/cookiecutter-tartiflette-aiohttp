import aiomysql

from {{cookiecutter.project_slug}}.config import config

__all__ = ("register_database_pool",)


async def register_database_pool(app: "aiohttp.web.Application") -> None:
    """
    Creates a MySQL pool and register it into the application.
    :param app: application to which register the MySQL pool
    :type app: aiohttp.web.Application
    """
    # pylint: disable=missing-yield-doc
    pool = await aiomysql.create_pool(
        host=config["database"]["host"],
        port=config["database"]["port"],
        user=config["database"]["user"],
        password=config["database"]["password"],
        db=config["database"]["database"],
        cursorclass=aiomysql.DictCursor,
    )
    app["database_pool"] = pool
    yield
    pool.close()
    await pool.wait_closed()
