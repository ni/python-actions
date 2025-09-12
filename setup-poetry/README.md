# `ni/python-actions/setup-poetry`

The `ni/python-actions/setup-poetry` action installs Poetry, adds it to the PATH, and caches it to
speed up workflows.

This action installs Poetry using the Python version that was selected by the
`ni/python-actions/setup-python` action, so you must call `ni/python-actions/setup-python` first.

By default, this action installs Poetry 2.1.4.

## Usage

```yaml
steps:
- uses: ni/python-actions/setup-python@v0.2
- uses: ni/python-actions/setup-poetry@v0.2
- run: poetry install -v
```

## Inputs

### `poetry-version`

```yaml
steps:
- uses: ni/python-actions/setup-python@v0.2
- uses: ni/python-actions/setup-poetry@v0.2
  with:
    poetry-version: 2.1.4
- run: poetry install -v
```

### `use-cache`

If you run into caching problems, you can disable caching by specifying `use-cache: false`.

## Outputs

### `cache-hit`

You can use `cache-hit` to check whether Poetry was loaded from cache. This is mainly intended for
testing the action.
