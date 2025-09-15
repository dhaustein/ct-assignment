# Makefile for the Unix Timestamp Converter Test Suite project.

.PHONY: help install generate-api-client lint lint-ruff lint-mypy format test test-api test-ui test-perf start-playwright-server stop-playwright-server download-k6

VENV_DIR := .venv
VENV_STAMP := $(VENV_DIR)/.synced
VENV_BIN := $(if $(VIRTUAL_ENV),$(VIRTUAL_ENV)/bin,$(VENV_DIR)/bin)
UV := $(VENV_BIN)/uv
K6_VERSION := $(shell cat packages/api/tests/perf/bin/.k6_version)

# Default target
.DEFAULT_GOAL := help

help:
	@echo "Makefile for the Unix Timestamp Converter Test Suite project"
	@echo ""
	@echo "Usage:"
	@echo "  make install                  - Create virtual environment and install dependencies"
	@echo "  make generate-api-client      - Generate the API SDK client"
	@echo "  make lint                     - Run all linters (ruff, mypy)"
	@echo "  make lint-ruff                - Run ruff linter"
	@echo "  make lint-mypy                - Run mypy type checker"
	@echo "  make format                   - Run ruff formatter"
	@echo "  make test                     - Run all tests (API and UI)"
	@echo "  make test-api                 - Run API tests"
	@echo "  make test-ui                  - Run UI E2E tests"
	@echo "  make test-perf                - Run performance tests"
	@echo "  make start-playwright-server  - Start the Playwright Docker container"
	@echo "  make stop-playwright-server   - Stop and remove the Playwright Docker container"
	@echo "  make download-k6              - Download the k6 binary for performance testing"
	@echo ""

# Installation
# set up the virtual environment and install dependencies
install: $(VENV_STAMP)

# ensures the venv exists and dependencies are synced
# uses a stamp file in the venv dir to track whether sync has been run
$(VENV_STAMP): pyproject.toml
	@if [ ! -d "$(VENV_DIR)" ]; then echo "Creating virtual environment at $(VENV_DIR)..."; uv venv; fi
	@echo "Syncing dependencies..."
	uv sync --all-extras --dev --all-packages
	@touch $(VENV_STAMP)

# API Client Generation
generate-api-client: install
	@echo "Generating API SDK client..."
	uv run --package api-sdk -- bash utils/generate-api-client.sh

# Linting
lint: lint-ruff lint-mypy

lint-ruff: install
	@echo "Running ruff linter..."
	uv run -- ruff check .

lint-mypy: install
	@echo "Running mypy type checker..."
	uv run -- mypy .

# Formatting
format: install
	@echo "Running ruff formatter..."
	uv run -- ruff format .

# Testing
test: test-api test-ui

test-api:
	@echo "Running API tests..."
	uv run --package api -- pytest -v -n auto packages/api/tests

test-ui: start-playwright-server
	@echo "Running UI E2E tests..."
	uv run --package frontend -- pytest -v packages/frontend/tests

start-playwright-server:
	@echo "Starting Playwright server..."
	podman run \
		--rm \
		--name playwright-server \
		-d \
		--ipc=host \
		-p 19323:19323 \
		--pull=newer \
		--replace \
		mcr.microsoft.com/playwright:v1.55.0-noble \
		npx playwright run-server --host 0.0.0.0 --port 19323

stop-playwright-server:
	@echo "Stopping and removing Playwright server..."
	podman stop playwright-server

test-perf: download-k6
	@echo "Running performance tests..."
	PATH="$(PWD)/packages/api/tests/perf/bin:$(PATH)" K6_WEB_DASHBOARD=true k6 run --linger --no-usage-report packages/api/tests/perf/test_perf_timestamp.js

download-k6:
	@echo "Downloading k6 binary..."
	K6_VERSION=$(cat packages/api/tests/perf/bin/.k6_version) && \
	echo "K6_VERSION is '${K6_VERSION}'" && \
		wget "https://github.com/grafana/k6/releases/download/v${K6_VERSION}/k6-v${K6_VERSION}-linux-amd64.tar.gz" -O - | \
		tar -xz -C packages/api/tests/perf/bin/ --strip-components=1
