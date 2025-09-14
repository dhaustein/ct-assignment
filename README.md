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

## Run performance tests (k6)

Download the k6 binary:

```sh
K6_VERSION=$(cat packages/api/tests/perf/bin/.k6_version) && \
wget "https://github.com/grafana/k6/releases/download/v${K6_VERSION}/k6-v${K6_VERSION}-linux-amd64.tar.gz" -O - | \
tar -xz -C packages/api/tests/perf/bin/ --strip-components=1
```
Note that this targets Linux specifically, the binaries for other OS-es are
different and you will want to download them from the k6 Release page manually.

Add k6 to your PATH:

```sh
PATH=$PATH:~/Temp/ct-assignment/packages/api/tests/perf/bin/
```

Run perf tests:

```sh
K6_WEB_DASHBOARD=true k6 run --linger --no-usage-report packages/api/tests/perf/test_perf_timestamp.js
```

This will return a link to the report web page, which will stay open until you
exit the process manually.
