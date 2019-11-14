from unittest.mock import patch

from {{cookiecutter.project_slug}}.utils import configure_logging, logging


def test_configure_logging():
    config_mock = {"conf1": "value1"}
    with patch.object(logging, "config", new={"logging": config_mock}):
        with patch(
            "{{cookiecutter.project_slug}}.utils.logging.logging.config.dictConfig"
        ) as dict_config_mock:
            configure_logging()
            dict_config_mock.assert_called_once_with(config_mock)
