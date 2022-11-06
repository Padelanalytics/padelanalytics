#!/bin/bash

if [ -z "$1" ] | [ -z "$2" ]; then
    echo use: $0 SOURCE_TAG DESTINATION_TAG
    echo SOURCE_TAG:      current running TAG
    echo DESTINATION_TAG: future running TAG after running this script
    echo example:         $0 0.0.1 0.0.2
    exit
fi

#####################
##### variables #####
#####################

SOURCE_TAG=$1
DESTINATION_TAG=$2

ROOT_IMAGE="paconte/padelanalytics-prod"
SOURCE_IMAGE_TAG="$ROOT_IMAGE:$SOURCE_TAG"
DESTINATION_IMAGE_TAG="$ROOT_IMAGE:$DESTINATION_TAG"
CONTAINER_NAME="padelanalytics-prod"

#####################
##### functions #####
#####################

purge_old_software_version () {
    if [[ -z "${ $CONTAINER_ID}" ]]; then
        echo Stoping conainer  $CONTAINER_ID
        docker stop $CONTAINER_ID

        echo Removing container $CONTAINER_ID
        docker rm $CONTAINER_ID
    fi

    if [[ -z "${ $IMAGE_ID}" ]]; then
        echo Removing image $IMAGE_ID
        docker image rm $IMAGE_ID
    fi
}

#####################
####### main ########
#####################

echo Setting up variables
CONTAINER_ID=$(docker ps -aqf "name=${CONTAINER_NAME}" -f status=running)
IMAGE_ID=$(docker inspect $CONTAINER_ID --format="{{.Image}}")

echo Proceding to remove running version $SOURCE_IMAGE_TAG and run version $DESTINATION_IMAGE_TAG

echo Docker login
docker login

echo Purge old software version
purge_old_software_version

echo Printing docker containers
docker ps

echo Starting new container with image $DESTINATION_IMAGE_TAG
docker run -it -p 8020:8020 padelanalytics-prod
