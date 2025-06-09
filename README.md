# `ni/python-actions`

`ni/python-actions` is a Git repository containing reusable GitHub Actions for NI Python projects.

## Table of Contents

- [`ni/python-actions`](#nipython-actions)
  - [Table of Contents](#table-of-contents)
  - [`ni/python-actions/setup-python`](#nipython-actionssetup-python)
    - [Usage](#usage)
    - [Inputs](#inputs)
      - [`python-version`](#python-version)
    - [Outputs](#outputs)
      - [`python-version`](#python-version-1)
      - [`python-path`](#python-path)
  - [`ni/python-actions/setup-poetry`](#nipython-actionssetup-poetry)
    - [Usage](#usage-1)
    - [Inputs](#inputs-1)
      - [`poetry-version`](#poetry-version)
  - [`ni/python-actions/check-project-version`](#nipython-actionscheck-project-version)
    - [Usage](#usage-2)
    - [Inputs](#inputs-2)
      - [`project-directory`](#project-directory)
      - [`expected-version`](#expected-version)
  - [`ni/python-actions/update-project-version`](#nipython-actionsupdate-project-version)
    - [Usage](#usage-3)
    - [Inputs](#inputs-3)
      - [`project-directory`](#project-directory-1)
      - [`branch-prefix`](#branch-prefix)
      - [`create-pull-request`](#create-pull-request)
      - [`version-rule` and `use-dev-suffix`](#version-rule-and-use-dev-suffix)
      - [`token`](#token)

## `ni/python-actions/setup-python`

The `setup-python` action installs Python and adds it to the PATH.

It is a thin wrapper for https://github.com/actions/setup-python which is intended to
single-source the default Python version for multiple NI Python projects.

By default, this action installs Python 3.11.9.

### Usage

```yaml
steps:
- uses: ni/python-actions/setup-python@v0.2
```

### Inputs

#### `python-version`

You can specify the `python-version` input for testing with multiple versions of Python:

```yaml
strategy:
  matrix:
    python-version: [3.9, '3.10', 3.11, 3.12, 3.13]
steps:
- uses: ni/python-actions/setup-python@v0.2
  with:
    python-version: ${{ matrix.python-version }}
```

### Outputs

#### `python-version`

You can use the `python-version` output to get the actual version of Python, which is useful for caching:

```yaml
steps:
- uses: ni/python-actions/setup-python@v0.2
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
- uses: ni/python-actions/setup-python@v0.2
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
- uses: ni/python-actions/setup-python@v0.2
- uses: ni/python-actions/setup-poetry@v0.2
- run: poetry install -v
```

### Inputs

#### `poetry-version`

```yaml
steps:
- uses: ni/python-actions/setup-python@v0.2
- uses: ni/python-actions/setup-poetry@v0.2
  with:
    poetry-version: 2.1.3
- run: poetry install -v
```

## `ni/python-actions/check-project-version`

The `check-project-version` action uses Poetry to get the version of a Python project and checks
that it matches an expected version. By default, this action checks against `github.ref_name`, which
is the GitHub release tag for GitHub release events.

This action requires Poetry, so you must call `setup-python` and `setup-poetry` first.

### Usage

```yaml
steps:
- uses: ni/python-actions/setup-python@v0.2
- uses: ni/python-actions/setup-poetry@v0.2
- uses: ni/python-actions/check-project-version@v0.2
  if: github.event_name == 'release'
```

### Inputs

#### `project-directory`

You can specify `project-directory` to check a project located in a subdirectory.

```yaml
- uses: ni/python-actions/check-project-version@v0.2
  with:
    project-directory: packages/foo
```

#### `expected-version`

You can specify `expected-version` to check against something other than `github.ref_name`.

```yaml
- uses: ni/python-actions/check-project-version@v0.2
  with:
    expected-version: ${{ steps.get-expected-version.outputs.version }}
```

## `ni/python-actions/update-project-version`

The `update-project-version` action uses Poetry to update the version of a Python project and
creates a pull request to modify its `pyproject.toml` file.

This action requires Poetry, so you must call `setup-python` and `setup-poetry` first.

Creating a pull request requires the workflow or job to have the following `GITHUB_TOKEN`
permissions:

```yaml
permissions:
  contents: write
  pull-requests: write
````

### Usage

```yaml
steps:
- uses: ni/python-actions/setup-python@v0.2
- uses: ni/python-actions/setup-poetry@v0.2
- uses: ni/python-actions/update-project-version@v0.2
```

### Inputs

#### `project-directory`

You can specify `project-directory` to update a project located in a subdirectory.

```yaml
- uses: ni/python-actions/update-project-version@v0.2
  with:
    project-directory: packages/foo
```

#### `branch-prefix`

You can specify `branch-prefix` to customize the pull request branch names. The default value of
`users/build/` generates pull requests with names like `users/build/update-project-version-main` and
`users/build/update-project-version-releases-1.1`.

```yaml
- uses: ni/python-actions/update-project-version@v0.2
  with:
    branch-prefix: users/python-build/
```

#### `create-pull-request`

You can use `create-pull-request` and `project-directory` to update multiple projects with a single
pull request.

```yaml
- uses: ni/python-actions/update-project-version@v0.2
  with:
    project-directory: packages/foo
    create-pull-request: false
- uses: ni/python-actions/update-project-version@v0.2
  with:
    project-directory: packages/bar
    create-pull-request: false
- uses: ni/python-actions/update-project-version@v0.2
  with:
    project-directory: packages/baz
    create-pull-request: true
```

#### `version-rule` and `use-dev-suffix`

You can specify `version-rule` and `use-dev-suffix` to customize the versioning scheme.

- `version-rule` specifies the rule for updating the version number. For example, `major` will
  update 1.0.0 -> 2.0.0, while `patch` will update 1.0.0 -> 1.0.1. See [the docs for `poetry
  version`](https://python-poetry.org/docs/cli/#version) for the list of rules and their behavior.
- `use-dev-suffix` specifies whether to use development versions like `1.0.0.dev0`.

The defaults are `version-rule=patch` and `use-dev-suffix=true`, which have the following behavior:

| Old Version | New Version |
| ----------- | ----------- |
| 1.0.0       | 1.0.1.dev0  |
| 1.0.1.dev0  | 1.0.1.dev1  |
| 1.0.1.dev1  | 1.0.1.dev2  |

When you are ready to exit the "dev" phase, you should manually update the version number to the
desired release version before creating a release in GitHub.

#### `token`

The default GITHUB_TOKEN cannot trigger PR workflows, so the generated pull request will not run any
status checks. You can work around this by using `token` to specify a token that is saved in a
repo/org secret.

See [Triggering further workflow
runs](https://github.com/peter-evans/create-pull-request/blob/main/docs/concepts-guidelines.md#triggering-further-workflow-runs)
in the `create-pull-request` action documentation for more info about this problem and other
solutions to it.
