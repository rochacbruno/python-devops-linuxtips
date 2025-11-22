#!/usr/bin/bash

# Install Trivy Operator
./kubectl apply -f https://raw.githubusercontent.com/aquasecurity/trivy-operator/main/deploy/static/trivy-operator.yaml

# List vulnerabilities
./kubectl get vulnerabilityreports -A

# Describe one
echo 'run:'
echo './kubectl describe vulnerabilityreport NAME -n default'
