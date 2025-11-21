#!/usr/bin/bash
IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' image-scanner-cluster-control-plane)

xdg-open http://$IP:32635/
