#!/bin/sh

# user defines
TEST_NAME="py_mb_cli"
PYTHON_VERSION="3.8"

# internal
APP_IMG_NAME=${TEST_NAME}_app_img

# run stack
docker build --build-arg BASE_IMAGE=python:${PYTHON_VERSION} -t ${APP_IMG_NAME} .
docker run --volume $(pwd):/app --rm -it ${APP_IMG_NAME}
