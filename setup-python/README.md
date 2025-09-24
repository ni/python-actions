# `ni/python-actions/setup-python`

The `ni/python-actions/setup-python` action installs Python and adds it to the PATH.

It is a thin wrapper for https://github.com/actions/setup-python which is intended to
single-source the default Python version for multiple NI Python projects.

By default, this action installs Python 3.11.9.

## Usage

> [!NOTE]
> These examples use `@v0`, but pinning to a commit hash or full release tag is recommended for
> build reproducibility and security.

```yaml
steps:
- uses: ni/python-actions/setup-python@v0
```

## Inputs

### `python-version` Input

You can specify the `python-version` input for testing with multiple versions of Python:

```yaml
strategy:
  matrix:
    python-version: [3.9, '3.10', 3.11, 3.12, 3.13]
steps:
- uses: ni/python-actions/setup-python@v0
  with:
    python-version: ${{ matrix.python-version }}
```

## Outputs

### `python-version` Output

You can use the `python-version` output to get the actual version of Python, which is useful for caching:

```yaml
steps:
- uses: ni/python-actions/setup-python@v0
  id: setup-python
- uses: actions/cache@v4
  with:
    path: .venv
    key: venv-${{ runner.os }}-py${{ steps.setup-python.outputs.python-version }}-${{ hashFiles('poetry.lock') }}
```

`python-version` is unique across implementations (CPython vs. PyPy) and free-threaded builds:

- CPython: "3.13.4".
- CPython with free-threading: "3.13.4t"
- PyPy: "pypy3.11.11-v7.3.19"

### `python-path`

`actions/setup-python` sets the `pythonLocation` environment variable to the **directory**
containing the Python installation.

You can also use the `python-path` output to get the path to the Python interpreter:

```yaml
steps:
- uses: ni/python-actions/setup-python@v0
  id: setup-python
- run: pipx install <package> --python ${{ steps.setup-python.outputs.python-version }}
```

## Environment Variables

### `pythonVersion`

This is the same as `outputs.python-version` and is mainly intended for use in
`ni/python-actions/setup-poetry`.
