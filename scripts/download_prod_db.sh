#!/bin/bash
# Copy the production database to the local machine.
# The container name must be padel_app, otherwise it will fail unless you change it in the below docker cp command
#
# Usage:
#  $ ./download_prod_db.sh

# Exit on first error
set -e

# Check if the PA_PROD_HOST environment variable is set
if [[ -z "${PA_PROD_HOST}" ]]; then
    echo "Environment variable PA_PROD_HOST is not set."
    exit 1
fi

echo $PA_PROD_HOST
# Extract the database from the production container
ssh $PA_PROD_HOST <<'ENDSSH'
#commands to run on remote host
docker cp padel_app:/django-padel/padelanalytics/db.sqlite3 /root/db.sqlite3
ENDSSH

# Copy the production database to the local machine
scp $PA_PROD_HOST:/root/db.sqlite3 ./db.sqlite3.prod
