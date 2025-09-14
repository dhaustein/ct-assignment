# Unix Timestamp Converter Test Suite

This project provides a test suite for the Unix timestamp converter at
[helloacm.com/tools/unix-timestamp-converter/](https://helloacm.com/tools/unix-timestamp-converter/).

## Installation

### Prerequisites

```
python3.13
uv
podman
```

This guide uses `podman`, but `docker` or any other compatible container runtime
can be substituted.

Check out the repository and install dependencies with:

```shell
uv venv
uv sync --all-extras --dev --all-packages
```

The `uv sync` command installs all dependencies for the entire monorepo,
enabling a developer to work across the whole codebase without further setup.

## Testing

### Generate API SDK

The API tests require a client to interact with the service. This client is
generated from the API's OpenAPI specification file using the `openapi-generator`.

```shell
uv run --package api-sdk -- bash utils/generate-api-client.sh
```

### Run API Tests (pytest, parallel)

Note: The API begins to rate-limit requests after approximately 10 attempts.

```shell
uv run --package api -- pytest -v -n auto packages/api/tests
```

The test run automatically outputs logs to the console and saves them to the
`packages/api/logs` directory.

### Run UI E2E Tests (Playwright)

This project uses the official Playwright Docker container to run browsers
for UI testing. This setup allows the local test runner to connect to the
browser server running inside the container, avoiding the need to install
browser binaries on the host machine.

Start the Playwright server:

```shell
podman run \
    --rm \
    --name playwright-server \
    -d \
    --ipc=host \
    -p 19323:19323 \
    --pull=always \
    mcr.microsoft.com/playwright:v1.55.0-noble \
    npx playwright run-server --host 0.0.0.0 --port 19323
```

Run the tests:

```shell
uv run --package frontend -- pytest -v packages/frontend/tests
```

Playwright traces will be saved to `/tmp/playwright_traces/`.

When testing is complete, stop and optionally remove the container:

```shell
podman stop playwright-server
podman rm playwright-server
```

### Run Performance Tests (k6)

Download the k6 binary:

```shell
K6_VERSION=$(cat packages/api/tests/perf/bin/.k6_version) && \
    wget "https://github.com/grafana/k6/releases/download/v${K6_VERSION}/k6-v${K6_VERSION}-linux-amd64.tar.gz" -O - | \
    tar -xz -C packages/api/tests/perf/bin/ --strip-components=1
```

Note: This command is specific to Linux. For other operating systems,
please download the appropriate binary from the k6 releases page.

Add k6 to your `PATH`:

```shell
export PATH="$PATH:$(pwd)/packages/api/tests/perf/bin/"
```

Run performance tests:

```shell
K6_WEB_DASHBOARD=true k6 run --linger --no-usage-report packages/api/tests/perf/test_perf_timestamp.js
```

Note: The API begins to rate-limit requests after approximately 10 attempts.

This command outputs a link to a web dashboard for the test report.
The dashboard will remain accessible until the process is manually terminated.

# Docs

Documentation related to this assignment is located in the `/docs` directory.

# TODOs

What is missing and should be added if this was a real project:

* Makefile or similar to wrap around the commands
* CI/CD pipeline that would trigger linting, testing, security scanning etc in new PRs
as well as the CD part for releases
* .devcontainer for easier distribution of the project
* EditorConfig for consistent coding style across the maintainers
* Optimized build/test processes for the monorepo (e.g., only test affected packages)
* IaC + observability stack for production deployment
