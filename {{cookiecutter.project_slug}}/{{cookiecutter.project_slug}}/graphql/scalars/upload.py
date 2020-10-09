from typing import Any

from aiohttp.web_request import FileField
from tartiflette import Scalar, TartifletteError
from tartiflette.language.ast.base import Node

__all__ = ("ScalarUpload",)


@Scalar("Upload")
class ScalarUpload:
    """Represents a file upload."""

    @staticmethod
    def coerce_output(value: Any) -> None:
        """Coerce the resolved value for output.

        :param value: value to coerce
        :type value: Any
        :raise TartifletteError: if used as output type
        """
        raise TartifletteError("Upload serialization unsupported.")

    @staticmethod
    def coerce_input(value: Any) -> FileField:
        """Coerce the input value from a variable value.

        :param value: value to coerce
        :type value: Any
        :return: the coerced value
        :rtype: FileField
        :raise TartifletteError: if value not a FileField instance
        """
        if isinstance(value, FileField):
            return value
        raise TartifletteError("Invalid uploaded file type.")

    @staticmethod
    def parse_literal(ast: Node) -> None:
        """Coerce the input value from an AST node.

        :param ast: AST node to coerce
        :type ast: Node
        :raise TartifletteError: if used as literal value
        """
        raise TartifletteError("Upload literal unsupported.")
