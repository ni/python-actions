# `ni/python-actions/analyze-project`

The `ni/python-actions/analyze-project` action analyzes the code quality
of a Python project using various linters and type checkers including
ni-python-styleguide, mypy (if the 'mypy' package is installed), and pyright
(if the 'pyright' package is installed).

This action requires Poetry, so you must call `ni/python-actions/setup-python` and
`ni/python-actions/setup-poetry` first.

## Usage

> [!NOTE]
> These examples use `@v0`, but pinning to a commit hash or full release tag is recommended for
> build reproducibility and security.

```yaml
steps:
- name: Check out repo
  uses: actions/checkout@v0
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

### `install-args`

If there are extra command-line arguments you need to install from your
pyproject.toml, specify them with this input. You can specify any arguments that
work with `poetry install` including `--extras` and `--with`. These
`install-args` will be appended to the basic command line which is `poetry
install -v`. Do not pass untrusted user input.

For example,

```yaml
- uses: ni/python-actions/analyze-project@v0
  with:
    project-directory: ${{ github.workspace }}/packages/myproject
    install-args: "--extras 'colors serialization' --with dev,docs,utils"
```
