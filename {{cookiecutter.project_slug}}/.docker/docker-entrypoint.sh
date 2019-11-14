#!/bin/sh

set -e

RETRY_MAX=30
RETRY_COUNT=0

is_database_ready() {
python << END
import asyncio
import sys

import aiomysql

from {{cookiecutter.project_slug}}.config import config


async def _connection_to_database():
    connection = await aiomysql.connect(
        host=config["database"]["host"],
        port=config["database"]["port"],
        user=config["database"]["user"],
        password=config["database"]["password"],
        db=config["database"]["database"],
    )
    connection.close()


try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_connection_to_database())
except Exception:
    sys.exit(-1)
sys.exit(0)
END
}

if [ "${DATABASE_IS_OPTIONAL}" != "1" ]
then
  until is_database_ready; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -gt $RETRY_MAX ]
    then
      >&2 echo "Unable to connect to the database."
      exit 1
    fi
    >&2 echo "Waiting connection to the database... (${RETRY_COUNT}/${RETRY_MAX})"
    sleep 1
  done
fi

exec "$@"
