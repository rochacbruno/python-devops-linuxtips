#!/usr/bin/bash
docker stop $(docker ps -a -q --filter "name=image") 
docker rm -f $(docker ps -a -q --filter "name=image") 
./kind delete cluster --name kind-image-scanner-cluster
docker rm -f $(docker ps -a -q --filter "name=kind") 
docker volume rm $(docker volume ls -q --filter "name=kind")
docker network rm kind

