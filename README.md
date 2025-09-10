Prerequisites: `python3.13`, `uv`

Install the project with uv
```shell
uv venv
uv sync --all-extras
```

Re-generate the API SDK
```shell
uv run --package api-sdk -- bash utils/generate-api-client.sh
```

Run API tests
```shell
uv run --package api -- pytest -v packages/api/tests/
```
