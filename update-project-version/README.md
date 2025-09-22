# `ni/python-actions/update-project-version`

The `ni/python-actions/update-project-version` action uses Poetry to update the version of a Python
project and creates a pull request to modify its `pyproject.toml` file. Publish workflows can use
this to update the version in `pyproject.toml` for the next build.

This action requires Poetry, so you must call `ni/python-actions/setup-python` and
`ni/python-actions/setup-poetry` first.

Creating a pull request requires the workflow or job to have the following `GITHUB_TOKEN`
permissions:

```yaml
permissions:
  contents: write
  pull-requests: write
````

## Usage

```yaml
steps:
- uses: ni/python-actions/setup-python@v0.2
- uses: ni/python-actions/setup-poetry@v0.2
- uses: ni/python-actions/update-project-version@v0.2
```

## Inputs

### `project-directory`

You can specify `project-directory` to update a project located in a subdirectory.

```yaml
- uses: ni/python-actions/update-project-version@v0.2
  with:
    project-directory: packages/foo
```

### `branch-prefix`

You can specify `branch-prefix` to customize the pull request branch names. The default value of
`users/build/` generates pull requests with names like `users/build/update-project-version-main` and
`users/build/update-project-version-releases-1.1`.

```yaml
- uses: ni/python-actions/update-project-version@v0.2
  with:
    branch-prefix: users/python-build/
```

### `create-pull-request`

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

### `version-rule` and `use-dev-suffix`

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

### `token`

The default GITHUB_TOKEN cannot trigger PR workflows, so the generated pull request will not run any
status checks. You can work around this by using `token` to specify a token that is saved in a
repo/org secret.

See [Triggering further workflow
runs](https://github.com/peter-evans/create-pull-request/blob/main/docs/concepts-guidelines.md#triggering-further-workflow-runs)
in the `create-pull-request` action documentation for more info about this problem and other
solutions to it.
