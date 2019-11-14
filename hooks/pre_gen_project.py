#!/usr/bin/env python
_PROJECT_SLUG = "{{ cookiecutter.project_slug }}"
_AUTHOR_NAME = "{{ cookiecutter.author_name }}"


def main():
    if not _PROJECT_SLUG.isidentifier():
        raise ValueError(
            f"Project slug < {_PROJECT_SLUG} > is not a valid Python "
            f"identifier."
        )

    if _PROJECT_SLUG != _PROJECT_SLUG.lower():
        raise ValueError(
            f"Project slug < {_PROJECT_SLUG} > should be all lowercase."
        )

    if "\\" in _AUTHOR_NAME:
        raise ValueError(
            f"Don't include backslashes in author name < {_AUTHOR_NAME} >."
        )


if __name__ == "__main__":
    main()
