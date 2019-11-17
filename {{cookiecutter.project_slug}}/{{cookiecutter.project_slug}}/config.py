from dynaconf import LazySettings

__all__ = ("config",)


config = LazySettings(
    MERGE_ENABLED_FOR_DYNACONF=True,
    ENVVAR_PREFIX_FOR_DYNACONF="{{cookiecutter.project_slug.upper()}}",
    ENVVAR_FOR_DYNACONF="{{cookiecutter.project_slug.upper()}}_SETTINGS_FILE",
    ROOT_PATH_FOR_DYNACONF="/",
    SETTINGS_FILE_FOR_DYNACONF=[
        "default.yml",
        "development.yml",
        "production.yml",
        "staging.yml",
        "testing.yml",
    ],
)
