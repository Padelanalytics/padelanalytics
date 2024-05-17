#!/bin/bash
# Copy the local database to the production machine
if [[ -z "${PA_PRODUCTION_HOST}" ]]; then
    echo "Environment variable PA_RODUCTION_HOST is not set."
    exit 1
fi

# Check argument has been passed
if [[ -z "${1}" ]]; then
    echo "File argument not passed."
    echo "Usage: $0 <file>"
    exit 1
fi

# Check if the file exists
if [ ! -f $1 ]; then
    echo "File $1 not found!"
    exit 1
fi

# Copy database to the production machine
scp $1 $PA_RODUCTION_HOST:/root/db.sqlite3

# Copy database to the production container
ssh $PA_RODUCTION_HOST <<'ENDSSH'
#commands to run on remote host
docker cp /root/db.sqlite3 padel_app:/django-padel/padelanalytics/db.sqlite3
ENDSSH

