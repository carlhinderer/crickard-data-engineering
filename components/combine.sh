#!/bin/bash

# Create combined docker-compose.yml
docker-compose -f nifi/docker-compose.yml \
               -f postgres/docker-compose.yml \
               config >> docker-compose.yml