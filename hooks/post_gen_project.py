#!/usr/bin/env python
import os
import re
import shutil

from tempfile import mkstemp

_PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

_PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
_OPEN_SOURCE_LICENSE = "{{ cookiecutter.open_source_license }}"
_MYSQL_VERSION = "{{ cookiecutter.mysql_version }}"


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


if __name__ == "__main__":
    main()
