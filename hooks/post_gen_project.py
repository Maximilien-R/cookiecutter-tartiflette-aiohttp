#!/usr/bin/env python
import os
import re
import shutil

from tempfile import mkstemp

_PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

_PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
_OPEN_SOURCE_LICENSE = "{{ cookiecutter.open_source_license }}"
_MYSQL_VERSION = "{{ cookiecutter.mysql_version }}"
_ADD_HEALTH_ROUTES = "{{ cookiecutter.add_health_routes }}"
_ADD_GRAPHIQL_ROUTE = "{{ cookiecutter.add_graphiql_route }}"
_ADD_SENTRY = "{{ cookiecutter.add_sentry }}"
_DEPLOYMENT = "{{ cookiecutter.deployment }}"


def _remove_files(files):
    if not isinstance(files, list):
        files = [files]

    for filepath in files:
        absolute_filepath = os.path.join(_PROJECT_DIRECTORY, filepath)
        if os.path.isfile(absolute_filepath):
            os.remove(absolute_filepath)
        elif os.path.isdir(absolute_filepath):
            shutil.rmtree(absolute_filepath)


def _remove_line_in_file(pattern, filepath):
    absolute_filepath = os.path.join(_PROJECT_DIRECTORY, filepath)
    if not os.path.isfile(absolute_filepath):
        return

    with open(absolute_filepath, "r") as source_file:
        _, output_file_path = mkstemp()
        with open(output_file_path, "w") as output_file:
            for line in source_file:
                if not re.match(pattern, line):
                    output_file.write(line)

        shutil.move(output_file_path, absolute_filepath)


def main():
    if _OPEN_SOURCE_LICENSE == "Not open source":
        _remove_files(["CONTRIBUTORS.md", "LICENSE"])

    if _OPEN_SOURCE_LICENSE != "GNU General Public License v3":
        _remove_files("COPYING")

    if _MYSQL_VERSION == "None":
        _remove_files(
            [
                ".docker",
                os.path.join(
                    _PROJECT_SLUG, "server", "registries", "database.py"
                ),
                os.path.join(_PROJECT_SLUG, "utils", "database.py"),
                os.path.join(
                    "tests",
                    "unit",
                    _PROJECT_SLUG,
                    "server",
                    "registries",
                    "test_database.py",
                ),
            ]
        )
        _remove_line_in_file(
            r"^aiomysql==[0-9]+\.[0-9]+\.[0-9]+$",
            os.path.join("requirements", "default.txt"),
        )

    if _ADD_HEALTH_ROUTES != "yes":
        _remove_files(
            [
                os.path.join(_PROJECT_SLUG, "server", "handlers", "health"),
                os.path.join("tests", "functional", _PROJECT_SLUG, "health",),
                os.path.join(
                    "tests",
                    "unit",
                    _PROJECT_SLUG,
                    "server",
                    "handlers",
                    "health",
                ),
            ]
        )

    if _ADD_GRAPHIQL_ROUTE != "yes":
        _remove_files(
            [
                os.path.join(_PROJECT_SLUG, "server", "handlers", "graphiql"),
                os.path.join(
                    "tests", "functional", _PROJECT_SLUG, "graphiql",
                ),
                os.path.join(
                    "tests",
                    "unit",
                    _PROJECT_SLUG,
                    "server",
                    "handlers",
                    "graphiql",
                ),
            ]
        )

    if _ADD_SENTRY != "yes":
        _remove_files(
            [
                os.path.join(_PROJECT_SLUG, "utils", "sentry.py"),
                os.path.join(
                    "tests", "unit", _PROJECT_SLUG, "utils", "test_sentry.py",
                ),
            ]
        )
        _remove_line_in_file(
            r"^sentry-sdk==[0-9]+\.[0-9]+\.[0-9]+$",
            os.path.join("requirements", "default.txt"),
        )

    if _DEPLOYMENT != "Heroku":
        _remove_files("heroku.yml")


if __name__ == "__main__":
    main()
