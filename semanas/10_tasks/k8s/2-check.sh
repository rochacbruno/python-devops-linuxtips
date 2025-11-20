#!/usr/bin/bash

./kubectl get nodes
./kubectl config get-contexts
./kubectl config use-context kind-image-scanner-cluster
./kubectl get pods -n kube-system
