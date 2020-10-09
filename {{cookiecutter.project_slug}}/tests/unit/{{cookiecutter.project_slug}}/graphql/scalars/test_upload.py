from unittest.mock import Mock

import pytest

from aiohttp.web_request import FileField
from multidict import CIMultiDict
from tartiflette import TartifletteError

from {{cookiecutter.project_slug}}.graphql.scalars.upload import ScalarUpload


def test_scalar_upload_coerce_output():
    with pytest.raises(
        TartifletteError, match="Upload serialization unsupported."
    ):
        ScalarUpload.coerce_output(None)


def test_scalar_upload_coerce_input():
    file_field = FileField(
        "name", "filename", Mock(), "content_type", CIMultiDict()
    )
    assert ScalarUpload.coerce_input(file_field) is file_field


def test_scalar_upload_coerce_input_error():
    with pytest.raises(TartifletteError, match="Invalid uploaded file type."):
        ScalarUpload.coerce_input(None)


def test_scalar_upload_parse_literal():
    with pytest.raises(TartifletteError, match="Upload literal unsupported."):
        ScalarUpload.parse_literal(None)
