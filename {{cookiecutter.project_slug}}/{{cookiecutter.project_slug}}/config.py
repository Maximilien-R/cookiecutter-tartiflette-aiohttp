from typing import Optional

from dynaconf import LazySettings
from dynaconf.base import Settings
from dynaconf.loaders import settings_loader

__all__ = ("config",)


def load(
    obj: Settings,
    env: Optional[str] = None,
    silent: bool = True,
    key: Optional[str] = None,
    filename: Optional[str] = None,
) -> None:
    """Load the appropriate YAML setting file related to the current env.

    :param obj: the settings instance
    :param env: settings current env (upper case)
    :param silent: if errors should raise
    :param key: if defined load a single key, else load all from `env`
    :param filename: Optional custom filename to load
    :type obj: Settings
    :type env: Optional[str]
    :type silent: bool
    :type key: Optional[str]
    :type filename: Optional[str]
    """
    # pylint: disable=unused-argument
    if env is None:
        return

    settings_loader(obj, filename=f"{env.lower()}.yml")


config = LazySettings(
    # dynaconf settings
    lowercase_read=True,
    merge_enabled=True,
    nested_separator="__",
    settings_files=["default.yml"],
    core_loaders=["YAML"],
    loaders=["{{cookiecutter.project_slug}}.config", "dynaconf.loaders.env_loader"],
    root_path=".",
    # environments settings
    environments=True,
    default_env="default",
    env="production",
    env_switcher="{{cookiecutter.project_slug.upper()}}_ENV",
    envvar_prefix="{{cookiecutter.project_slug.upper()}}",
    envvar="{{cookiecutter.project_slug.upper()}}_SETTINGS_FILE",
    # dotenv settings
    load_dotenv=True,
    dotenv_override=False,
    dotenv_path=".",
)
