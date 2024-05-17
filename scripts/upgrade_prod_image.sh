#!/bin/bash
# Upgrade the running production image
#
# Usage:
#  $ ./upgrade_prod_db param1
# * param1: the image tag to upgrade to

# Exit on first error
set -e

usage() {
    cat <<EOM
    Usage:
    $0 <image_tag>

EOM
    exit 0
}
[ -z $1 ] && { usage; }


# Check if the PA_PROD_HOST environment variable is set
if [[ -z "${PA_PROD_HOST}" ]]; then
    echo "Environment variable PA_PROD_HOST is not set."
    exit 1
fi

# Check argument has been passed
if [[ -z "${1}" ]]; then
    echo "File argument not passed."
    echo "Usage: $0 <file>"
    exit 1
fi

# Check argument is a valid image tag
if ! [[ "${1}" =~ ^[0-9]{1}\.[0-9]{1}\.[0-9]{1}$ ]]; then
    echo "${1} is not a valid image tag."
    echo "Image tag must follow the regex: ^[0-9]{1}\.[0-9]{1}\.[0-9]{1}$"
    exit 1
fi

# Upgrade the running production image
ssh $PA_PROD_HOST <<ENDSSH
#commands to run on remote host
docker pull paconte/padelanalytics:$1
docker stop padel_app
docker rm padel_app
docker run -d --restart unless-stopped -p 8030:8030 --name padel_app paconte/padelanalytics:$1
docker ps | grep padel_app
ENDSSH
