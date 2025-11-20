#!/usr/bin/bash
docker exec image-scanner-cluster-control-plane crictl images | grep image-scanner

