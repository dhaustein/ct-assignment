#!/usr/bin/env bash

#
# Generates the Python API client from the OpenAPI specification
#
# This script performs the following steps:
# 1. Checks for the`openapi-generator-cli` python dependency
# 2. Validates the OpenAPI specification file
# 3. Cleans up the output directory before generation
# 4. Generates the API client SDK
#

set -o errexit
set -o pipefail
set -o nounset

PACKAGE_NAME="api_sdk"
PACKAGE_SRC_DIR="libs/$PACKAGE_NAME/src"
API_SPEC_FILE="packages/api/src/api/unix-timestamp-converter-spec.yml"
API_GEN_CONFIG_FILE="utils/api-gen-config.yml"

echo "INFO: Starting API client generation..."

echo "INFO: Checking for openapi-generator-cli..."
if ! command -v openapi-generator-cli &> /dev/null; then
    echo "ERROR: openapi-generator-cli must be installed to proceed!" >&2
    exit 1
fi
echo "INFO: openapi-generator-cli found."

echo "INFO: Validating API specification file: $API_SPEC_FILE..."
if ! openapi-generator-cli validate -i "$API_SPEC_FILE"; then
    echo "ERROR: API specification validation failed." >&2
    exit 1
fi
echo "INFO: API specification is valid."

echo "INFO: Cleaning up output directory: $PACKAGE_SRC_DIR/$PACKAGE_NAME"
# Delete all files and directories inside, except for py.typed
find "$PACKAGE_SRC_DIR/$PACKAGE_NAME" -mindepth 1 ! -name "py.typed" -delete
echo "INFO: Cleanup complete."

echo "INFO: Generating Python API client from $API_SPEC_FILE..."
openapi-generator-cli generate \
    -i "$API_SPEC_FILE" \
    -g python \
    -c "$API_GEN_CONFIG_FILE" \
    -o "$PACKAGE_SRC_DIR" \
    --additional-properties=packageName="$PACKAGE_NAME" \
    --skip-validate-spec \

echo "INFO: API client generated successfully in $PACKAGE_SRC_DIR/$PACKAGE_NAME"
