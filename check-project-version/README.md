# `ni/python-actions/check-project-version`

The `ni/python-actions/check-project-version` action uses Poetry to get the version of a Python
project and checks that it matches an expected version. Publish workflows can use this to verify
that the release tag matches the version number in `pyproject.toml`.

By default, this action checks against `github.ref_name`, which is the GitHub release tag for GitHub
release events.

This action requires Poetry, so you must call `ni/python-actions/setup-python` and
`ni/python-actions/setup-poetry` first.

## Usage

> [!NOTE]
> These examples use `@v0`, but pinning to a commit hash or full release tag is recommended for
> build reproducibility and security.

```yaml
steps:
- uses: ni/python-actions/setup-python@v0
- uses: ni/python-actions/setup-poetry@v0
- uses: ni/python-actions/check-project-version@v0
  if: github.event_name == 'release'
```

## Inputs

### `project-directory`

You can specify `project-directory` to check a project located in a subdirectory.

```yaml
- uses: ni/python-actions/check-project-version@v0
  with:
    project-directory: packages/foo
```

### `expected-version`

You can specify `expected-version` to check against something other than `github.ref_name`.

```yaml
- uses: ni/python-actions/check-project-version@v0
  with:
    expected-version: ${{ steps.get-expected-version.outputs.version }}
```
