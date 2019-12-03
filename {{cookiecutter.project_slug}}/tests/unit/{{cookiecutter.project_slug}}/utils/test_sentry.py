from unittest.mock import Mock, patch

import pytest

from tartiflette import TartifletteError

from {{cookiecutter.project_slug}}.utils import (
    configure_sentry,
    sentry,
    sentry_error_coercer,
)


def test_configure_sentry():
    config_mock = {"dsn": "dsn"}
    aiohttp_integration_mock = Mock()
    logging_integration_mock = Mock()
    with patch.object(sentry, "config", new={"sentry": config_mock}):
        with patch(
            "{{cookiecutter.project_slug}}.utils.sentry.sentry_sdk"
        ) as sentry_sdk_mock:
            with patch(
                "{{cookiecutter.project_slug}}.utils.sentry.AioHttpIntegration",
                return_value=aiohttp_integration_mock,
            ):
                with patch(
                    "{{cookiecutter.project_slug}}.utils.sentry.LoggingIntegration",
                    return_value=logging_integration_mock,
                ):
                    configure_sentry()
                    sentry_sdk_mock.init.assert_called_once_with(
                        dsn="dsn",
                        integrations=[
                            logging_integration_mock,
                            aiohttp_integration_mock,
                        ],
                    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    (
        "exception",
        "error",
        "capture_exception_called",
        "capture_exception_response",
        "logged",
    ),
    [
        (Mock(), {"message": "Exception"}, False, False, False,),
        (
            Mock(original_error=Exception("Exception")),
            {"message": "Exception"},
            True,
            True,
            False,
        ),
        (
            Mock(original_error=Exception("Exception")),
            {"message": "Exception"},
            True,
            False,
            True,
        ),
        (
            Mock(original_error=TartifletteError("TartifletteError")),
            {"message": "TartifletteError"},
            True,
            True,
            False,
        ),
        (
            Mock(original_error=TartifletteError("TartifletteError")),
            {"message": "TartifletteError"},
            True,
            False,
            True,
        ),
    ],
)
async def test_sentry_error_coercer(
    exception,
    error,
    capture_exception_called,
    capture_exception_response,
    logged,
):
    with patch(
        "{{cookiecutter.project_slug}}.utils.sentry.sentry_sdk",
    ) as sentry_sdk_mock:
        sentry_sdk_mock.capture_exception = Mock(
            return_value=capture_exception_response
        )

        with patch(
            "{{cookiecutter.project_slug}}.utils.sentry.logger",
        ) as logger_mock:
            assert await sentry_error_coercer(exception, error) == error
            if capture_exception_called:
                sentry_sdk_mock.capture_exception.assert_called_once_with(
                    exception.original_error
                )
            else:
                sentry_sdk_mock.capture_exception.assert_not_called()

            if logged:
                logger_mock.exception.assert_called_once_with(
                    "Unhandled error.", exc_info=exception.original_error
                )
            else:
                logger_mock.exception.assert_not_called()
