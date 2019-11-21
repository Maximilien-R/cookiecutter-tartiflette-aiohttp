from unittest.mock import patch, Mock

from {{cookiecutter.project_slug}}.utils import configure_sentry, sentry


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
                        ]
                    )
