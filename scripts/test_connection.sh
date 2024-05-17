#!/bin/bash
# Test the server is reachable and available to talk with
#
# Usage:
#  $bash ./test_connection

# Exit on first error
set -e

# Check if the PA_PROD_HOST environment variable is set
if [[ -z "${PA_PROD_HOST}" ]]; then
    echo "Environment variable PA_RODUCTION_HOST is not set."
    exit 1
fi

ssh $PA_PROD_HOST <<'ENDSSH'
#commands to run on remote host
echo "Hello from the remote host!"
ENDSSH
