# `ni/python-actions`

`ni/python-actions` is a Git repository containing reusable GitHub Actions for NI Python projects.

## Actions

- [`ni/python-actions/setup-python`](setup-python): installs Python and adds it to the PATH,
  single-sourcing the default Python version for multiple NI Python projects.
- [`ni/python-actions/setup-poetry`](setup-poetry): installs Poetry, adds it to the PATH, and caches
  it to speed up workflows.
- [`ni/python-actions/check-project-version`](check-project-version): uses Poetry to get the version
  of a Python project and checks that it matches an expected version. Publish workflows can use this
  to verify that the release tag matches the version number in `pyproject.toml`.
- [`ni/python-actions/update-project-version`](update-project-version): uses Poetry to update the
  version of a Python project and creates a pull request to modify its `pyproject.toml` file.
  Publish workflows can use this to update the version in `pyproject.toml` for the next build.
