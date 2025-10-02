#!/usr/bin/env bash
#
# lint.sh - OpenAPI Specification Linting Script
#
# Description:
#   This script validates the Venice.ai OpenAPI specification file using two
#   industry-standard linting tools: Spectral and Redocly CLI. It ensures the
#   specification adheres to OpenAPI 3.0.0 standards and best practices.
#
# Usage:
#   ./lint.sh
#
# Prerequisites:
#   - Node.js and npm must be installed
#   - Dependencies must be installed: npm install
#
# Exit Codes:
#   0 - All linting checks passed successfully
#   1 - One or more linting checks failed
#
# Linters Used:
#   1. Spectral: Validates OpenAPI spec against rules defined in spectral.yaml
#   2. Redocly CLI: Performs additional validation and style checks
#
# Environment Variables:
#   SPEC - Path to the OpenAPI specification file (default: venice.openapi.v3.yaml)
#
# Author: Venice.ai API Reference Team
# Last Modified: 2025-10-02
#

# Exit immediately if any command fails, treat unset variables as errors,
# and propagate pipe failures
set -euo pipefail

# Specification file to lint
SPEC="venice.openapi.v3.yaml"

# Step 1: Run Spectral linting
# Spectral checks the OpenAPI specification against rules defined in spectral.yaml
# and the built-in OpenAPI ruleset
echo "[1/2] Spectral lint..."
npx spectral lint "$SPEC" --verbose

# Step 2: Run Redocly linting
# Redocly performs additional validation and checks for best practices
echo "[2/2] Redocly lint..."
npx @redocly/cli lint "$SPEC"

# Success message
echo "✅ Linting complete."