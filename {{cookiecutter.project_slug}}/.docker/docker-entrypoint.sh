#!/bin/sh

set -e

RETRY_MAX=30
RETRY_COUNT=0

is_database_ready() {
python << END
import asyncio
import sys

import aiomysql

from {{cookiecutter.project_slug}}.utils import extract_database_credentials


async def _connection_to_database():
    database_credentials = extract_database_credentials()
    connection = await aiomysql.connect(
        host=database_credentials["host"],
        port=database_credentials["port"],
        user=database_credentials["user"],
        password=database_credentials["password"],
        db=database_credentials["database"],
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
