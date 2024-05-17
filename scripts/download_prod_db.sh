#!/bin/bash
# Copy the production database to the local machine
# The container name must be padel_app, otherwise it will fail unless you change it in the below docker cp command
if [[ -z "${PA_PRODUCTION_HOST}" ]]; then
    echo "Environment variable PA_RODUCTION_HOST is not set."
    exit 1
fi

ssh $PA_RODUCTION_HOST <<'ENDSSH'
#commands to run on remote host
docker cp padel_app:/django-padel/padelanalytics/db.sqlite3 /root/db.sqlite3
ENDSSH
scp $PA_RODUCTION_HOST:/root/db.sqlite3 ./db.sqlite3.prod