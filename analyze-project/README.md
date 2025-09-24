# `ni/python-actions/analyze-project`

The `ni/python-actions/update-project-version` action analyzes the code quality
of a Python project using various linters and type checkers including
ni-python-styleguide, mypy (if the 'mypy' package is installed), and pyright
(if the 'pyright' package is installed).

This action requires Poetry, so you must call `ni/python-actions/setup-python` and
`ni/python-actions/setup-poetry` first.

## Usage

```yaml
steps:
- uses: ni/python-actions/setup-python@v0
- uses: ni/python-actions/setup-poetry@v0
- uses: ni/python-actions/analyze-project@v0
```

## Inputs

### `project-directory`

You can specify `project-directory` to indicate the location of the pyproject.toml
file associated with the Python project you are analyzing.

```yaml
- uses: ni/python-actions/update-project-version@v0
  with:
    project-directory: ${{ github.workspace }}/packages/myproject
```

### `extras`

If there are extras you need to install from your pyproject.toml, specify a space-separated list
of extra groups to install. For example, 

```yaml
- uses: ni/python-actions/analyze-project@v0
  with:
    project-directory: ${{ github.workspace }}/packages/myproject
    extras: 'docs drivers'
```
