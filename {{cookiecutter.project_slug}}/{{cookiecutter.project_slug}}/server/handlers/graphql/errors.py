from typing import Any, Dict

from tartiflette.utils.errors import is_coercible_exception, to_graphql_error

__all__ = ("format_error",)


def format_error(exception: Exception) -> Dict[str, Any]:
    """Format an exception into a formatted GraphQL error.

    :param exception: the exception to format
    :type exception: Exception
    :return: a formatted GraphQL error
    :rtype: Dict[str, Any]
    """
    if not is_coercible_exception(exception):
        exception = to_graphql_error(exception)
    return exception.coerce_value()
