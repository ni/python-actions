# `ni/python-actions/check-project-links`

This action searches a project tree for `pyproject.toml` files, extracts `https://` links from those files, and validates each discovered URL by making an HTTP request in a Docker container. It fails only when a checked URL returns a `4xx` response. `2xx` and `3xx` responses are treated as successful and logged without failing the action.

## Inputs

### `project-directory`

Path to the directory containing one or more `pyproject.toml` files.

Default: `${{ github.workspace }}`

### `docker-image`

Docker image used to perform the HTTP requests.

Default: `curlimages/curl:8.22.0`

> [!NOTE]
> The action default uses a full digest sha. Although the action does not require this.

## Examples

> [!NOTE]
> These examples use `@v0`, but pinning to a commit hash or full release tag is recommended for
> build reproducibility and security.


```yaml
steps:
  - uses: actions/checkout@v0

  - name: Check project links
    uses: ni/python-actions/check-project-links@v1
    with:
      project-directory: .
      docker-image: curlimages/curl:8.22.0
```

## Behavior

- Uses `rg` to locate `pyproject.toml` files beneath the configured project directory.
- Extracts every `https://...` URL that ends at the first whitespace character.
- Deduplicates the list of URLs and writes them to a temporary file.
- Validates each URL with the configured Docker image.
- Logs `2xx` and `3xx` responses as passing.
- Fails the action only when a URL returns a `4xx` status code.
- Other status codes are considered a warning.
