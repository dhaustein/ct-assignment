Prerequisites:

```
python3.13
uv
podman
```

I use `podman` here but `docker` or similar should work, too.

## Install the project with uv
```shell
uv venv
uv sync --all-extras --dev --all-packages
```

Note on the long `sync` command - this will install __all__ dependencies for the whole
monorepo so a developer can work across the entire codebase in one go.

## Re-generate the API SDK

For the API tests to work, they need an API client to use. Here we generate it
using the `openapi-generator` using the api's spec file as reference.

```shell
uv run --package api-sdk -- bash utils/generate-api-client.sh
```

## Run API tests (pytest, in parallel)

```shell
uv run --package api -- pytest -v -n auto packages/api/tests
```

The test run automatically outputs logs to console as we as the
`packages/api/logs` directory.

## Run UI E2E tests (Playwright)

For UI testing, this project runs the browsers inside the official Playwright
Docker container.

The local test runner will connect to its containerized browser server.

This avoids installing browser binaries on the host machine.

Start the Playwright server:

```sh
podman run --rm --name playwright-server -d --ipc=host -p 19323:19323 mcr.microsoft.com/playwright:v1.55.0-noble npx playwright run-server --host 0.0.0.0 --port 19323
```

Run the tests:

```sh
uv run --package frontend -- pytest -v packages/frontend/tests
```

Playwright traces will be saved into `/tmp/playwright_traces/`

When done testing, stop and (if wanted) remove the container:

```sh
podman stop playwright-server
podman rm playwright-server
```
