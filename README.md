# `ni/python-actions`

`ni/python-actions` is a Git repository containing reusable GitHub Actions for NI Python projects.

## `ni/python-actions/setup-python`

The `setup-python` action installs Python and adds it to the PATH.

It is a thin wrapper for https://github.com/actions/setup-python which is intended to
single-source the default Python version for multiple NI Python projects.

By default, this action installs Python 3.11.9.

### Usage

```yaml
steps:
- uses: ni/python-actions/setup-python@v0.1.0
```

### Inputs

#### `python-version`

You can specify the `python-version` input for testing with multiple versions of Python:
```yaml
strategy:
  matrix:
    python-version: [3.9, '3.10', 3.11, 3.12, 3.13]
steps:
- uses: ni/python-actions/setup-python@v0.1.0
  with:
    python-version: ${{ matrix.python-version }}
```

### Outputs

#### `python-version`

You can use the `python-version` output to get the actual version of Python, which is useful for caching:
```yaml
steps:
- uses: ni/python-actions/setup-python@v0.1.0
  id: setup-python
- uses: actions/cache@v4
  with:
    path: .venv
    key: venv-${{ runner.os }}-py${{ steps.setup-python.outputs.python-version }}-${{ hashFiles('poetry.lock') }}
```

#### `python-path`

`actions/setup-python` sets the `pythonLocation` environment variable to the **directory**
containing the Python installation.

You can also use the `python-path` output to get the path to the Python interpreter:
```yaml
steps:
- uses: ni/python-actions/setup-python@v0.1.0
  id: setup-python
- run: pipx install <package> --python ${{ steps.setup-python.outputs.python-version }}
```

## `ni/python-actions/setup-poetry`

The `setup-poetry` action installs Poetry, adds it to the PATH, and caches it to speed up
workflows. 

This action installs Poetry using the Python version that was selected by the `setup-python`
action, so you must call `setup-python` first.

By default, this action installs Poetry 1.8.2.

### Usage

```yaml
steps:
- uses: ni/python-actions/setup-python@v0.1.0
- uses: ni/python-actions/setup-poetry@v0.1.0
- run: poetry install -v
```

### Inputs

#### `poetry-version`

```yaml
steps:
- uses: ni/python-actions/setup-python@v0.1.0
- uses: ni/python-actions/setup-poetry@v0.1.0
  with:
    poetry-version: 2.1.3
- run: poetry install -v
```