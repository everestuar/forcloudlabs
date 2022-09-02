#!/usr/bin/env bash

## Dockerfile.38-ms17-v1
docker build -t pyodbc-38-v1 -f Dockerfile.38-ms17-v1 .
docker run --rm --entrypoint bash -v $PWD:/local pyodbc-38-v1 -c "cp -R /opt /local"

## Dockerfile.38-ms17-v2
docker build -t pyodbc-38-v2 -f Dockerfile.38-ms17-v2 .
docker run --rm --entrypoint bash -v $PWD:/local pyodbc-38-v2 -c "cp -R /opt /local"
# search for pyodbc-layer-38-v2.zip in opt directory located inside your current directory
