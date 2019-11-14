import pytest

from tartiflette import TartifletteError
from tartiflette.language.ast import Location

from {{cookiecutter.project_slug}}.server.handlers.graphql.errors import format_error


@pytest.mark.parametrize(
    "exception,expected",
    [
        (
            Exception("Exception"),
            {"locations": [], "message": "Exception", "path": None},
        ),
        (
            ValueError("ValueError"),
            {"locations": [], "message": "ValueError", "path": None},
        ),
        (
            TypeError("TypeError"),
            {"locations": [], "message": "TypeError", "path": None},
        ),
        (
            TartifletteError("TartifletteError"),
            {"locations": [], "message": "TartifletteError", "path": None},
        ),
        (
            TartifletteError("TartifletteError", path=["parent", "leaf"]),
            {
                "locations": [],
                "message": "TartifletteError",
                "path": ["parent", "leaf"],
            },
        ),
        (
            TartifletteError(
                "TartifletteError",
                locations=[
                    Location(line=1, column=0, line_end=2, column_end=20,)
                ],
            ),
            {
                "locations": [{"column": 0, "line": 1}],
                "message": "TartifletteError",
                "path": None,
            },
        ),
        (
            TartifletteError(
                "TartifletteError", extensions={"extra": "value"}
            ),
            {
                "extensions": {"extra": "value"},
                "locations": [],
                "message": "TartifletteError",
                "path": None,
            },
        ),
    ],
)
def test_format_error(exception, expected):
    result = format_error(exception)
    assert result == expected
