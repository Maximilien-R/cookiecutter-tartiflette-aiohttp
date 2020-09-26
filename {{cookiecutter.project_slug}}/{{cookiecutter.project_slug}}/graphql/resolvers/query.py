from typing import Any, Dict, Optional

from tartiflette import Resolver

__all__ = ("resolve_query_hello",)


@Resolver("Query.hello")
async def resolve_query_hello(
    parent: Optional[Dict[str, Any]],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> str:
    """Resolve the "Query.hello" field.

    :param parent: initial value provided to the GraphQL execute method
    :param args: computed arguments related to the resolved field
    :param ctx: context provided to the GraphQL engine execute method
    :param info: information related to the execution and resolved field
    :type parent: Optional[Dict[str, Any]]
    :type args: Dict[str, Any]
    :type ctx: Dict[str, Any]
    :type info: ResolveInfo
    :return: the computed field value
    :rtype: Optional[Dict[str, Any]]
    """
    # pylint: disable=unused-argument
    return f"Hello {args['name']}!"
