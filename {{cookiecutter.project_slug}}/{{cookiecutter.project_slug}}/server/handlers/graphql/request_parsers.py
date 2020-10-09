import json

from typing import Any, Dict, List, Optional, Tuple, Union

from aiohttp import web
from aiohttp.http_exceptions import HttpBadRequest
from aiohttp.web_request import FileField
from multidict import MultiDictProxy

__all__ = ("extract_graphql_params",)


async def _graphql_request_parser(request: web.Request) -> Dict[str, Any]:
    """Parse an application/graphql content type request.

    :param request: incoming aiohttp request
    :type request: web.Request
    :return: GraphQL params extracted from the request
    :rtype: Dict[str, Any]
    """
    return {"query": await request.text()}


async def _json_request_parser(request: web.Request) -> Dict[str, Any]:
    """Parse an application/json content type request.

    :param request: incoming aiohttp request
    :type request: web.Request
    :return: GraphQL params extracted from the request
    :rtype: Dict[str, Any]
    :raise HttpBadRequest: if the body is an invalid JSON
    """
    try:
        return await request.json()
    except Exception as e:
        raise HttpBadRequest(message="POST body sent invalid JSON.") from e


async def _form_urlencoded_request_parser(
    request: web.Request,
) -> Dict[str, Any]:
    """Parse an application/x-www-form-urlencoded content type request.

    :param request: incoming aiohttp request
    :type request: web.Request
    :return: GraphQL params extracted from the request
    :rtype: Dict[str, Any]
    """
    return await request.post()


def _inject_file_to_operations(
    operations: Union[Dict[str, Any], List[Any]],
    file_instance: FileField,
    current_path: List[str],
    full_path: str,
) -> Union[FileField, Dict[str, Any]]:
    """Inject the file instance in operations according to the path.

    :param operations: operations on which inject the file
    :param file_instance: the file instance to inject
    :param current_path: current path to follow to inject the file
    :param full_path: the raw full path used
    :type operations: Union[Dict[str, Any], List[Any]]
    :type file_instance: FileField
    :type current_path: List[str]
    :type full_path: str
    :return: the operations to update or the file instance
    :rtype: Union[FileField, Dict[str, Any]]
    :raise HttpBadRequest: if the operations doesn't fit with the path
    """
    if not current_path:
        if operations is not None:
            raise HttpBadRequest(
                f"Path < {full_path} > in < map > multipart field doesn't "
                f"lead to a null value."
            )
        return file_instance

    key = current_path[0]

    try:
        index = int(key)
    except ValueError as e:
        if not isinstance(operations, dict):
            raise HttpBadRequest(
                f"Key < {key} > from path < {full_path} > doesn't lead to an "
                "object."
            ) from e
        operations[key] = _inject_file_to_operations(
            operations[key], file_instance, current_path[1:], full_path
        )
    else:
        if not isinstance(operations, list):
            raise HttpBadRequest(
                f"Index < {index} > from path < {full_path} > doesn't lead to "
                "a list."
            )
        operations[index] = _inject_file_to_operations(
            operations[index], file_instance, current_path[1:], full_path
        )
    return operations


def _extract_multipart_params(
    data: MultiDictProxy,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Validate and extract the operations and map fields from the data.

    :param data: the data from which extract fields
    :type data: MultiDictProxy
    :return: the operations and map fields
    :rtype: Tuple[Dict[str, Any], Dict[str, Any]]
    :raise HttpBadRequest: if missing or invalid fields
    """
    if "operations" not in data:
        raise HttpBadRequest("Missing multipart field < operations >.")

    if "map" not in data:
        raise HttpBadRequest("Missing multipart field < map >.")

    try:
        operations = json.loads(data["operations"])
    except Exception as e:
        raise HttpBadRequest(
            "Invalid JSON in the < operations > multipart field."
        ) from e
    else:
        if not isinstance(operations, dict):
            raise HttpBadRequest(
                "Invalid type for the < operations > multipart field."
            )

    try:
        files_map = json.loads(data["map"])
    except Exception as e:
        raise HttpBadRequest(
            "Invalid JSON in the < map > multipart field."
        ) from e
    else:
        if not isinstance(files_map, dict):
            raise HttpBadRequest(
                "Invalid type for the < map > multipart field."
            )

    return operations, files_map


async def _form_data_request_parser(request: web.Request) -> Dict[str, Any]:
    """Parse a multipart/form-data content type request.

    :param request: incoming aiohttp request
    :type request: web.Request
    :return: GraphQL params extracted from the request
    :rtype: Dict[str, Any]
    :raise HttpBadRequest: if file paths are invalid
    """
    data = await request.post()

    operations, files_map = _extract_multipart_params(data)

    for field_name, paths in files_map.items():
        if not isinstance(paths, list):
            raise HttpBadRequest(
                "Invalid type for the < map > multipart field entry key "
                f"< {field_name} > array."
            )

        for index, path in enumerate(paths):
            if not isinstance(path, str):
                raise HttpBadRequest(
                    "Invalid type for the < map > multipart field entry key "
                    f"< {field_name} > array index < {index} > value."
                )

            operations = _inject_file_to_operations(
                operations, data.get(field_name), path.split("."), path
            )

    return operations


_REQUEST_PARSERS = {
    "application/graphql": _graphql_request_parser,
    "application/json": _json_request_parser,
    "application/x-www-form-urlencoded": _form_urlencoded_request_parser,
    "multipart/form-data": _form_data_request_parser,
}


async def _parse_request(request: web.Request) -> Dict[str, Any]:
    """Parse a GraphQL request depending on the content type.

    :param request: incoming aiohttp request
    :type request: web.Request
    :return: GraphQL params extracted from the request
    :rtype: Dict[str, Any]
    """
    request_parser = _REQUEST_PARSERS.get(request.content_type)
    if request_parser:
        return await request_parser(request)
    return {}


def _parse_graphql_params(
    body_data: Dict[str, Any], url_data: Dict[str, Any]
) -> Tuple[str, Optional[Dict[str, Any]], Optional[str]]:
    """Validate and extract GraphQL params from request body or URL.

    :param body_data: data extracted from the body request
    :param url_data: data extracted from the query string
    :type body_data: Dict[str, Any]
    :type url_data: Dict[str, Any]
    :return: a tuple containing the query, variables and operation name
    :rtype: Tuple[str, Optional[Dict[str, Any]], Optional[str]]
    :raise HttpBadRequest: if the filled in variables are invalid JSON
    """
    query = url_data.get("query") or body_data.get("query")
    if not isinstance(query, str):
        query = None

    variables = url_data.get("variables") or body_data.get("variables")
    if variables and isinstance(variables, str):
        try:
            variables = json.loads(variables)
        except Exception as e:
            raise HttpBadRequest("Variables are invalid JSON.") from e
    elif not isinstance(variables, dict):
        variables = None

    operation_name = url_data.get("operationName") or body_data.get(
        "operationName"
    )
    if not isinstance(operation_name, str):
        operation_name = None

    return (query, variables, operation_name)


async def extract_graphql_params(
    request: web.Request,
) -> Tuple[str, Optional[Dict[str, Any]], Optional[str]]:
    """Parse and extract GraphQL params from a request.

    :param request: incoming aiohttp request
    :type request: web.Request
    :return: a tuple containing the query, variables and operation name
    :rtype: Tuple[str, Optional[Dict[str, Any]], Optional[str]]
    """
    return _parse_graphql_params(await _parse_request(request), request.query)
